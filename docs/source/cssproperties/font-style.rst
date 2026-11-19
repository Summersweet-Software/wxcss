font-style
=============

There are a few different allowed font-style specifiers. I will list them all.

.. code-block:: python

    # wxcss/internals.py
    _FONT_STYLE_MAP = {
        "normal": wx.FONTSTYLE_NORMAL,
        "oblique": wx.FONTSTYLE_SLANT,
        "italic": wx.FONTSTYLE_ITALIC,
    }


How To Use
------------


.. code-block:: css

    Notebook {
        font-style: "normal";
    }
