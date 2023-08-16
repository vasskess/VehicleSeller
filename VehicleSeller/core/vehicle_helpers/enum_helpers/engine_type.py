from enum import Enum

from VehicleSeller.core.choices_mixin import ChoicesMixin
from VehicleSeller.core.max_length_mixin import MaxLengthMixin


class EngineTypes(ChoicesMixin, MaxLengthMixin, Enum):
    Diesel = "Diesel"
    Petrol = "Petrol"
    LPG = "LPG"
    Electric = "Electric"
    Hybrid = "Hybrid"
