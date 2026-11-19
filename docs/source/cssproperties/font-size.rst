font-size
===========

Wxcss supports the :code:`font-size` property as well. We currently only support :code:`px` and :code:`pt` units.
All other units will throw an error during application-time.


.. admonition:: Important

    Note that the :code:`px` units apply to the *vertical* size only!

How To Use
------------

.. code-block:: css

    Notebook {
        font-size: 52pt;
    }