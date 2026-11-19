from typing import NamedTuple, Protocol

from cssutils.css import (
    CSSStyleRule,
    ColorValue,
    DimensionValue,
    Property,
    PropertyValue,
    Value,
)
import wx


class CustomizedCSSElementClass(Protocol):
    """A class with a customized CSS element selector name"""

    __css_element_name__: str


class WidgetWithCSSClasses(Protocol):
    """A widget containing multiple css classes."""

    __css_classes__: list[str]


def get_css_element_name(cls: CustomizedCSSElementClass | type) -> str:
    """Get the element name used for CSS selectors"""
    if hasattr(cls, "__css_element_name__"):
        return cls.__css_element_name__
    return getattr(cls, "__name__")


def get_css_element_names(cls: CustomizedCSSElementClass | type) -> list[str]:
    """Get all element names used for CSS selectors"""
    return [
        get_css_element_name(cls),
        *(get_css_element_name(base) for base in cls.mro()),
    ]


def get_css_classes(window: WidgetWithCSSClasses | wx.Window) -> list[str]:
    """get all css classes on a widget"""
    if hasattr(window, "__css_classes__"):
        return getattr(window, "__css_classes__")
    return []


def all_classes_match(
    incoming_classes, window: WidgetWithCSSClasses | wx.Window
) -> bool:
    """Checks if all incoming_classes are found on a wx.Window object."""
    return all(incoming in get_css_classes(window) for incoming in incoming_classes)


_FONT_WEIGHTS_MAP = {
    "normal": wx.FONTWEIGHT_NORMAL,
    "bold": wx.FONTWEIGHT_BOLD,
    "bolder": wx.FONTWEIGHT_EXTRABOLD,
    "extra-bold": wx.FONTWEIGHT_EXTRABOLD,
    "light": wx.FONTWEIGHT_LIGHT,
    "lighter": wx.FONTWEIGHT_EXTRALIGHT,
    "extra-light": wx.FONTWEIGHT_EXTRALIGHT,
    "heavy": wx.FONTWEIGHT_HEAVY,
    "heavier": wx.FONTWEIGHT_EXTRAHEAVY,
    "extra-heavy": wx.FONTWEIGHT_EXTRAHEAVY,
}

_FONT_STYLE_MAP = {
    "normal": wx.FONTSTYLE_NORMAL,
    "oblique": wx.FONTSTYLE_SLANT,
    "italic": wx.FONTSTYLE_ITALIC,
}


class WxCssAutoCreated(NamedTuple):
    created_for: wx.Window


# TODO: break this out into a dll so we can have a speedup [very slow code :(]
def create_or_update_spacer(
    sizer: wx.Sizer,
    children: wx.SizerItemList,
    index: int,
    window: wx.Window,
    value: int,
):
    if (
        (len(children) - 1 > index)
        and (children[index].IsSpacer())
        and (type(children[index].UserData) == WxCssAutoCreated)
        and (children[index].UserData.created_for is window)
    ):
        children[index].GetSpacer().Set(value, value)
    else:
        item = sizer.InsertSpacer(index, value)
        item.SetUserData(WxCssAutoCreated(window))


class ApplicationFunctions:
    """A Namespace containing all functions used for application if properties"""

    @staticmethod
    def simple_application_spec(*spec: type[Value]):
        def decorator(func):
            def wrapper(window: wx.Window, value: PropertyValue):
                if value.length != len(spec):
                    raise ValueError(value)
                for value_item, spec_item in zip(value, spec):
                    if not isinstance(value_item, spec_item):
                        raise TypeError(value_item, "Expected", spec_item)

                return func(window, tuple(value))

            return wrapper

        return decorator

    @simple_application_spec(ColorValue)
    @staticmethod
    def apply_background_color(window: wx.Window, value: tuple[ColorValue]):
        window.SetBackgroundColour(
            wx.Colour(
                int(value[0].red),
                int(value[0].green),
                int(value[0].blue),
                alpha=int(value[0].alpha),
            )
        )

    @simple_application_spec(ColorValue)
    @staticmethod
    def apply_foreground_color(window: wx.Window, value: tuple[ColorValue]):
        window.SetForegroundColour(
            wx.Colour(
                int(value[0].red),
                int(value[0].green),
                int(value[0].blue),
                alpha=int(value[0].alpha),
            )
        )

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_font_size(window: wx.Window, value: tuple[DimensionValue]):
        css_size = value[0]

        if css_size.dimension == "pt":
            font = window.GetFont()
            font.SetPointSize(int(css_size.value))
            window.SetFont(font)
        elif css_size.dimension == "px":
            font = window.GetFont()
            font.SetPixelSize((0, css_size.value))
            window.SetFont(font)
        else:
            raise TypeError(css_size, "Expected value in pt or px units")

    @simple_application_spec(Value)
    @staticmethod
    def apply_font_weight(window: wx.Window, value: tuple[Value]):
        css_weight = value[0]

        if css_weight.value not in _FONT_WEIGHTS_MAP.keys():
            raise ValueError(css_weight)

        font = window.GetFont()
        font.SetWeight(_FONT_WEIGHTS_MAP[css_weight.value])
        window.SetFont(font)

    @simple_application_spec(Value)
    @staticmethod
    def apply_font_family(window: wx.Window, value: tuple[Value]):
        css_family = value[0]

        font = window.GetFont()
        font.SetFaceName(css_family.value)
        window.SetFont(font)

    @simple_application_spec(Value)
    @staticmethod
    def apply_font_style(window: wx.Window, value: tuple[Value]):
        css_style = value[0]

        if css_style.value not in _FONT_STYLE_MAP.keys():
            raise ValueError(css_style)

        font = window.GetFont()
        font.SetStyle(_FONT_STYLE_MAP[css_style.value])
        window.SetFont(font)

    @staticmethod
    def apply_text_decoration(window: wx.Window, value: PropertyValue):
        font = window.GetFont()
        for deco in value:
            if deco.value == "none":
                font.SetUnderlined(False)
                font.SetStrikethrough(False)
            if deco.value == "underline":
                font.SetUnderlined(True)
            if deco.value == "line-through":
                font.SetStrikethrough(True)
        window.SetFont(font)

    @simple_application_spec(Value)
    @staticmethod
    def apply_content(window: wx.Window, value: tuple[Value]) -> bool:
        """Applies "content" to various widgets. Can be hijacked to support more widget types.
        Returns :py:const:`True` if the widget was already handled."""
        match window:
            case wx.StaticText():
                window.SetLabelText(value[0].value)
            case wx.TextCtrl():
                window.SetValue(value[0].value)
            case wx.Button():
                window.SetLabelText(value[0].value)
            case _:
                return False
        return True

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_margin(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")

        if window.GetParent() is None:
            return
        sizer = window.GetParent().GetSizer()
        if sizer is None:
            return

        children = sizer.GetChildren()
        for c, item in enumerate(children):
            if item.IsWindow() and item.GetWindow().Id == window.Id:
                # apply or update right margin
                create_or_update_spacer(sizer, children, c + 1, window, value[0].value)
                # apply or update left margin
                create_or_update_spacer(sizer, children, c - 1, window, value[0].value)
                break

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_margin_left(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")

        if window.GetParent() is None:
            return
        sizer = window.GetParent().GetSizer()
        if sizer is None:
            return

        children = sizer.GetChildren()
        for c, item in enumerate(children):
            if item.IsWindow() and item.GetWindow().Id == window.Id:
                create_or_update_spacer(sizer, children, c - 1, window, value[0].value)
                break

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_margin_right(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")

        if window.GetParent() is None:
            return
        sizer = window.GetParent().GetSizer()
        if sizer is None:
            return

        children = sizer.GetChildren()
        for c, item in enumerate(children):
            if item.IsWindow() and item.GetWindow().Id == window.Id:
                create_or_update_spacer(sizer, children, c + 1, window, value[0].value)
                break

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_padding(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        sizer = window.GetSizer()
        if sizer is None:
            return
        children = sizer.GetChildren()
        if len(children) > 0:
            # Insert at beginning if entry does not exist
            create_or_update_spacer(sizer, children, 0, window, value[0].value)

            # insert at end if entry doesnt exist
            create_or_update_spacer(sizer, children, -1, window, value[0].value)
        else:
            item = sizer.AddSpacer(value[0].value)
            item.SetUserData(WxCssAutoCreated(window))

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_max_width(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        window.SetMaxSize(wx.Size(value[0].value, window.GetMaxHeight()))

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_max_height(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        window.SetMaxSize(wx.Size(window.GetMaxWidth(), value[0].value))

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_min_width(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        window.SetMinSize(wx.Size(value[0].value, window.GetMinHeight()))

    @staticmethod
    def apply_min_height(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        window.SetMinSize(wx.Size(window.GetMinWidth(), value[0].value))

    @simple_application_spec(DimensionValue)
    @staticmethod
    def apply_width(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        x, y = window.GetPositionTuple()
        window.SetDimensions(x, y, value[0].value, window.GetSize().Height)

    @staticmethod
    def apply_height(window: wx.Window, value: tuple[DimensionValue]):
        if value[0].dimension != "px":
            raise TypeError(value[0].value, "Expected value in px units")
        x, y = window.GetPositionTuple()
        window.SetDimensions(x, y, window.GetSize().Width, value[0].value)

    _mapping = {
        "background-color": apply_background_color,
        "color": apply_foreground_color,
        "font-size": apply_font_size,
        "font-weight": apply_font_weight,
        "font-family": apply_font_family,
        "font-style": apply_font_style,
        "text-decoration": apply_text_decoration,
        "content": apply_content,
        "margin": apply_margin,
        "margin-left": apply_margin_left,
        "margin-right": apply_margin_right,
        "padding": apply_padding,
        "max-width": apply_max_width,
        "max-height": apply_max_height,
        "min-width": apply_min_width,
        "min-height": apply_min_height,
        "width": apply_width,
        "height": apply_height,
    }


def apply_css_rule(rule: CSSStyleRule, window: wx.Window):
    property: Property
    for property in rule.style:
        if property.name not in ApplicationFunctions._mapping.keys():
            continue
        ApplicationFunctions._mapping[property.name](window, property.propertyValue)
