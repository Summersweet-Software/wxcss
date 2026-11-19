from cssutils.css import (
    CSSComment,
    CSSRule,
    CSSRuleList,
    CSSStyleRule,
    CSSStyleSheet,
    Selector,
)
import wx
import cssutils

from wxcss import internals


def apply_css(css_data: str, window: wx.Window):
    stylesheet: CSSStyleSheet = cssutils.parseString(css_data)

    def _apply_css_recur(
        window: wx.Window, previously_applied_rules: list[CSSStyleRule]
    ):
        window_selector_name = internals.get_css_element_names(window.__class__)
        rules: CSSRuleList = stylesheet.cssRules
        applied_rules = [*previously_applied_rules]

        # apply rules of parents
        rule: CSSRule
        for rule in applied_rules:
            internals.apply_css_rule(rule, window)

        for rule in rules:
            match rule:
                case CSSStyleRule():
                    selector: Selector
                    for selector in rule.selectorList:
                        element = selector.element
                        should_apply = (
                            element is None or element[1] in window_selector_name
                        )

                        selector_parts = selector.selectorText.split(".")[1:]
                        should_apply = should_apply and internals.all_classes_match(
                            selector_parts, window
                        )

                        if should_apply:
                            internals.apply_css_rule(rule, window)
                            applied_rules.append(rule)

                case CSSComment():
                    pass
                case _:
                    print(rule, type(rule))

        for child in window.Children:
            _apply_css_recur(child, applied_rules)

    _apply_css_recur(window, [])
