from enum import Enum

from VehicleSeller.core.choices_mixin import ChoicesMixin
from VehicleSeller.core.max_length_mixin import MaxLengthMixin


class Transmission(ChoicesMixin, MaxLengthMixin, Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    CVT = "CVT"
    SEMI_AUTOMATIC = "Semi-Automatic"
