Selectors
===========

wxcss currently supports 2 kinds of selectors.

Element Selectors
-------------------

Element selectors are applied using class names or :py:attr:`__css_element_name__` if it exists.
Sub-classing is supported. For example, selecting all :code:`Window` elements will select everything subclassing :py:class:`wx.Window`

Class Selectors
-----------------

Class selectors are supported exactly how you think they would be.
You can also combine class selectors by doing the following.

.. code-block:: css

    .my-class.my-class-2 {
        /* applied to elements containing both classes */
    }


Element + Class Selectors
---------------------------

You can also combine element and class/multi-class selectors

.. code-block:: css

    Notebook.my-class {
        /* applied to elements that subclass Notebook and have the `my-class` css class */
    }

Multi-Selection
-----------------

You can also say that a rule applies to more than one single selector.

.. code-block:: css

    Notebook.my-class, Frame {
        /* applied to elements that subclass Notebook and have the `my-class` css class
        OR subclass Frame */
    }

Star-Selector
---------------

Despite being unnecessary, wxcss also supports using the :code:`*` selector.
The other way to achieve this is to use the :code:`Window` selector.

.. code-block:: css

    * {
        /* applies to everything. */
    }