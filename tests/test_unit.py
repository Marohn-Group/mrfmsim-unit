from mrfmsim_unit.unit import MRFMQuantity, MRFMUnitRegistry, MRFMSIM_SYSTEM
from dataclasses import dataclass, field
from pint import UnitRegistry
import numpy as np


class TestDefaultSystem:
    """Test add default mrfmsim system to the registry."""

    def test_default_system_method1(self):
        """Test the default system of the MRFMUnitRegistry class."""

        ureg = UnitRegistry(system="mrfmsim")
        ureg.System.from_definition(MRFMSIM_SYSTEM)

        q = 1 * ureg.tesla
        assert q.to_base_units().magnitude == 1000
        q = 1 * ureg.attonewton
        assert np.isclose(q.to_base_units().magnitude, 1, rtol=1e-15)

    def test_default_system_method2(self):
        """Test the default system of the MRFMUnitRegistry class."""

        ureg = UnitRegistry()
        ureg.System.from_definition(MRFMSIM_SYSTEM)
        ureg.default_system = "mrfmsim"

        q = 1 * ureg.tesla
        assert q.to_base_units().magnitude == 1000
        q = 1 * ureg.attonewton
        assert np.isclose(q.to_base_units().magnitude, 1, rtol=1e-15)


def test_MRFMQuantity():
    """Test the MRFMQuantity class.

    Check that the base_magnitude function returns the correct value.
    """

    ureg = UnitRegistry()
    q = MRFMQuantity(1.0, ureg.nanometer)
    assert q.magnitude == 1.0
    assert q.base_magnitude == 1.0e-9
    assert q.bm == 1.0e-9


def test_MRFMUnitRegistry():
    """Test the MRFMUnitRegistry class.

    Check that the default system and format are set correctly.
    """

    mureg = MRFMUnitRegistry()
    assert mureg.default_system == "mrfmsim"
    assert mureg.default_format == "~P"

    # check the base units are millitesla, nanometer, attonewton, kelvin, second
    assert (1.0 * mureg.tesla).to_base_units().magnitude == 1000
    # causes floating point rounding error
    assert np.isclose((1.0e-9 * mureg.m).to_base_units().m, 1, rtol=1e-15)
    assert np.isclose((1.0e-9 * mureg.newton).to_base_units().m, 1e9, rtol=1e-15)
    # check other units
    assert (1.0 * mureg.s).to_base_units().m == 1.0
    # test the default format
    assert str(1.0 * mureg.meter / mureg.second) == "1.0 m/s"


def test_MRFMUnitRegistry_getattr():
    """Test the getattr method of MRFMUnitRegistry"""

    @dataclass
    class Component:
        a: int = field(metadata={"unit": "m"})
        b: float = field(metadata={"unit": "mT"})
        c: float = 1

        def __post_init__(self):
            self.d = 2

    mureg = MRFMUnitRegistry()
    component = Component(1, 2.0)
    assert mureg.getattr(component, "a") == 1 * mureg.m
    assert mureg.getattr(component, "b") == 2.0 * mureg.mT
    assert mureg.getattr(component, "c") == 1
    assert mureg.getattr(component, "d") == 2


def test_MRFMUnitREgistry_base_magnitude():
    """Test the base_magnitude property of MRFMUnitRegistry's Quanity"""

    mureg = MRFMUnitRegistry()
    # test the base units are millitesla, nanometer, attonewton, kelvin, second
    assert np.isclose((1 * mureg.m).bm, 1.0e9, rtol=1e-15)
    assert np.isclose((1 * mureg.T).bm, 1000, rtol=1e-15)
    assert np.isclose((1e-9 * mureg.N).bm, 1e9)
