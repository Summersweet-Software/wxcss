border-style-right
==================

The :code:`border-style-right` property works by setting :py:const:`wx.RIGHT | wx.BORDER_SIMPLE` flag for the given window.
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
        border-style-right: solid;
    }