font-weight
=============

There are a few different allowed font-weight specifiers. I will list them all.

.. code-block:: python

    # wxcss/internals.py
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


How To Use
------------


.. code-block:: css

    Notebook {
        font-weight: bolder;
    }
