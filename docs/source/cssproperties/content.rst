content
=========

Wxcss lets you apply the :code:`content` to only a small subset of window-types so far.

Supported
-----------

- :py:class:`wx.StaticText`
- :py:class:`wx.TextCtrl`
- :py:class:`wx.Button`

How To Use
------------

.. code-block:: css

    TextCtrl {
        content: "Some Text";
    }


Extending Supported Items
---------------------------

The following code is an example to allow you to extend the amount of supported windows that apply content.

.. code-block:: python

    import wxcss.internals
    import cssutils
    import wx


    class MyCustomWindow(wx.Window):
        ...

        def set_value(self, value):
            ...


    @wxcss.internals.ApplicationFunctions.simple_application_spec(cssutils.css.value.Value)
    def custom_apply_content(window: wx.Window, value: tuple[cssutils.css.value.Value]):
        # premature return if default function already handled it.
        if wxcss.internals.ApplicationFunctions.apply_content(window, value):
            return True

        match window:
            case MyCustomWindow():
                window.set_value(value[0].value)
            case _:
                # return false if we couldn't handle it here
                return False
        # return true if we handled it
        return True


    # replace handler for `content` with our custom handler
    wxcss.internals.ApplicationFunctions._mapping["content"] = custom_apply_content
    