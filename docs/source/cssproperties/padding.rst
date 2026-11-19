padding
=========

The :code:`padding` property works by applying spacers at the beginning and end of the window's sizer.
It currently only supports :code:`px` units.


.. admonition:: Warning

    This property is laggy on a large-scale! It works by applying spacers where necessary!

How To Use
------------

.. code-block:: css

    Notebook {
        padding: 10px;
    }