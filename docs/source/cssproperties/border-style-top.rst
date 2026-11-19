border-style-top
==================

The :code:`border-style-top` property works by setting :py:const:`wx.TOP | wx.BORDER_SIMPLE` flag for the given window.
It currently only supports :code:`px` units.

Supported Styles
------------------
- none
- solid (:py:const:`wx.BORDER_SIMPLE`)

.. admonition:: Warning

    This is mostly work-in-progress and may change a little as time goes on.

How To Use
------------

.. code-block:: css

    TextCtrl {
        border-style-top: solid;
    }