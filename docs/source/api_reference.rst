API Reference
===============

.. py:currentmodule:: wxcss


.. py:function:: set_class(window: wx.Window, cls_name: str)

    Adds a class to window's class list (contained in :py:attr:`__css__classes__`)


.. py:function:: apply_css(css_data: str, window: wx.Window)

    Recursively applies css to a window and all of its children.

    If a rule is applied to a window, then all children will automatically have that rule applied.

