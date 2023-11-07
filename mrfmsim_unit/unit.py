from pint import UnitRegistry
from dataclasses import asdict

__mrfmsim_plugin__ = ['MRFMUnitRegistry', 'MRFMQuantity']

class MRFMQuantity(UnitRegistry.Quantity):

    @property
    def base_magnitude(self):
        """Return the magnitude of the quantity in the base units of the registry.
        """
        return self.to_base_units().magnitude
    
    @property
    def bm(self):
        """Return the magnitude of the quantity in the base units of the registry.

        bm is short for base_magnitude.
        """
        return self.base_magnitude


class MRFMUnitRegistry(UnitRegistry):
    """Custom MRFM unit registry with default base units."""

    Quantity = MRFMQuantity

    _BASE_UNITS = {
        "ampere": {"microampere": 1.0},
        "meter": {"nanometer": 1.0},
        "gram": {"microgram": 1.0},
        "kelvin": {"kelvin": 1.0},
        "second": {"second": 1.0},
    }

    def _after_init(self):
        """Set the default unit system and format."""

        super()._after_init()
        mrfm_system = self.get_system("mrfmsim")
        mrfm_system.base_units = self._BASE_UNITS

        self.default_system = "mrfmsim"
        self.default_format = "~P"

 
    def getattr(self, dc_obj, attr):
        """Get the value and unit of a dataclass object.

        The variable requires to have the metadata defined with
        the "unit" key. Otherwise, only the value is returned.
        
        :param dc_obj: dataclass object
        :param attr: attribute name
        """
        if attr not in asdict(dc_obj):
            return getattr(dc_obj, attr)
        else:
            unit_str = dc_obj.__dataclass_fields__[attr].metadata.get("unit", "")
            return getattr(dc_obj, attr) * self(unit_str)
