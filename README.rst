mrfmsim-unit
============

The *mrfmsim-unit* package is a part of the
`mrfmsim project <https://marohn-group.github.io/mrfmsim-docs/>`__. 
The package provides a set of units
that is natural to the mrfmsim problems while avoiding rounding errors. 
The package should be used with the unit package `pint <https://pint.readthedocs.io/en/stable/>`__.



Installation
------------

To install the *mrfmsim-unit* package::

    pip install .

To test the *mrfmsim-unit* package::

    tox


Usage
-----

Several packages support mathematical calculations with units, such as *Pint* and *SymPy*.
However, these packages output the quantity in customized Python objects. These objects
create overhead during the computation and are incompatible with certain operations
in *Numpy* and *Numba* packages that *mrfmsim* relies on. Therefore, the decision was not to
allow custom unit objects during the *mrfmsim* computations. Instead, a set of base units
is used, and the *mrfmsim* package allows unit definition in the components' metadata and 
experiment nodes' metadata. The *mrfmsim-unit* plugin serves as an ancillary tool to display
and convert units before and after the calculations. The plugin should be used with the
*pint* and *mrfmsim* packages.

The base units defined for the *pint* unit system:
- nanometer
- microampere
- microgram
- second
- kelvin

There are two ways to handle units in the *mrfmsim* package. 

``MRFMUnitRegistry`` as the registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``MRFMUnitRegistry`` registry provides the base unit system, shortened unit format, and
the ``getattr`` method to extract the unit from the component metadata. 

.. code-block:: python

    from mrfmsim.unit import MRFMUnitRegistry

    # create the unit registry
    mureg = MRFMUnitRegistry()

    # create a component with units
    field = 1.0 * mureg.T

    # get the magnitude of the field (pint method)
    >>> field.m # or field.magnitude
    1.0

    # get the value in terms of base units
    >>> field.to_base_units()
    1000.0 µg/(s^2 µA)

    # get the magnitude of the field in the mrfmsim default units (mrfmsim-unit method)
    >>> field.bm # or field.base_magnitude or field.to_base_units().magnitude
    1000.0

    # output component metadata for any parameter in dataclass with metadata field defined

    @dataclass
    class Component:
        a: int = field(metadata={"unit": "m"})
        b: float = field(metadata={"unit": "mT"})

    component = Component(1, 2.0)

    # get the a attribute in the component object
    >>> mureg.getattr(component, "a")
    >>> 1 m

Add unit system to ``UnitRegistry``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *pint* package does not allow operations between different unit registry classes.
For existing workflows incorporating the ``UnitRegistry``, we provide the customized
"mrfmsim" system containing the base units. However, the additional formatting and 
``getattr`` method is not available. To add the mrfmsim unit system to the ``UnitRegistry``.

.. code-block:: python

    from pint import UnitRegistry
    from mrfmsim_unit.unit import MRFMSIM_SYSTEM

    # create the unit registry
    ureg = UnitRegistry(system="mrfmsim")
    ureg.System.from_definition(MRFMSIM_SYSTEM)

or 

.. code-block:: python

    from pint import UnitRegistry
    from mrfmsim_unit.unit import MRFMSIM_SYSTEM

    # create the unit registry
    ureg = UnitRegistry()
    ureg.System.from_definition(MRFMSIM_SYSTEM)
    ureg.default_system = "mrfmsim"

To convert a 1 Tesla field to 1 millitesla:

.. code-block:: python

    # unit quantity
    field = 1.0 * ureg.T # telsa to millitesla

    # get the field value in base units
    >>> field.to_base_units()
    1000.0 microgram/(microampere second^2)

    # get the magnitude of the field in base units
    >>> field.to_base_units().magnitude # or field.magnitude
    1000.0


Units
-----

The  base units mrfmsim systems (default) uses are:

* position :math:`(x,y,z)`: :math:`\mathrm{nm}`
* current: :math:`I`: :math:`\mathrm{\mu A}`
* mass :math:`m`: :math:`\mathrm{\mu g}` 
* time :math:`t`: :math:`\mathrm{s}` 
* fields :math:`B_z` and :math:`B_1`: :math:`\mathrm{mT} = 1 \times 10^{-3} \: \mathrm{T}`
* force: :math:`F`: :math:`\mathrm{aN} = 1 \times 10^{-18} \: \mathrm{N}`
* temperature :math:`T`: :math:`\mathrm{K}`

Units which follow from these choices include:

* volume element :math:`dV`: :math:`\mathrm{nm}^{-3}`
* frequency :math:`f`: :math:`\mathrm{Hz}`
* gyromagnetic ratio :math:`\gamma_{\mathrm{p}}` and :math:`\gamma_{\mathrm{e}}`: :math:`\mathrm{s}^{-1} \: \mathrm{mT}^{-1}`
* field derivative :math:`\partial B_z / \partial x`: :math:`\mathrm{mT} \: \mathrm{nm}^{-1}`
* field second derivative :math:`\partial^2 B_z / \partial x^2`: :math:`\mathrm{mT} \: \mathrm{nm}^{-2}`
* spin density :math:`\rho`: :math:`\mathrm{nm}^{-3}`
* magnetic moment :math:`\mu_{\text{p}}` and :math:`\mu_{\text{e}}`: :math:`\mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1}` 

In these units, the electron gyromagnetic ratio [#NISTgammae]_ is 

.. math::

    \gamma_e & = 1.760 859 708 \times 10^{11} \: \mathrm{s}^{-1} \: \mathrm{T}^{-1} \\
             & = 1.760 859 708 \times 10^{8} \: \mathrm{s}^{-1} \: \mathrm{mT}^{-1},

the electron magnetic moment [#NISTmue]_ is 

.. math::

    \mu_e & = -928.476 430 \times 10^{-26} \: \mathrm{J} \: \mathrm{T}^{-1} \\
          & = -9.28 \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1},
    
the proton gyromagnetic ratio [#NISTgammap]_ is

.. math::

    \gamma_p & = 2.675 222 005 \times 10^{8} \: \mathrm{s}^{-1} \: \mathrm{T}^{-1} \\
             & = 2.675 222 005 \times 10^{5} \: \mathrm{s}^{-1} \: \mathrm{mT}^{-1},

and the proton magnetic moment is

.. math::

    \mu_p &= 1.410 606 743 \times 10^{-26} \: \mathrm{J} \: \mathrm{T}^{-1} \\
          &= 0.0141 \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1}.

The gyromagnetic ratios were taken from the NIST database and do not account for
any chemical shift corrections.  It is pleasing to find that in our unit system, 
the electron and proton magnetic moments come out to be numbers of order one!

In the calculations below, we will need the following two physical constants. 
In terms of our practical units,  
        
.. math::
            
    \hbar &= \text{Planck's constant divided by } 2 \pi \\
          &= 1.054571628 \times 10^{-34} \: \mathrm{J} \: \mathrm{s} \\
          &= 1.054571628 \times 10^{-7} \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{s} \\
    k_b &= \text{Boltzmann's constant} \\
        &= 1.3806504 \times 10^{-23} \: \mathrm{J} \: \mathrm{K}^{-1} \\
        &= 1.3806504 \times 10^{4} \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{K}^{-1}

**References**

.. [#NISTgammae] http://physics.nist.gov/cgi-bin/cuu/Value?gammae
.. [#NISTgammap] http://physics.nist.gov/cgi-bin/cuu/Value?gammap
.. [#NISTmue] http://physics.nist.gov/cgi-bin/cuu/Value?muem
.. [#NISTmup] http://physics.nist.gov/cgi-bin/cuu/Value?mup
