from enum import Enum

from VehicleSeller.core.choices_mixin import ChoicesMixin
from VehicleSeller.core.max_length_mixin import MaxLengthMixin


class EuroCategory(ChoicesMixin, MaxLengthMixin, Enum):
    EURO1 = "EURO-1"
    EURO2 = "EURO-2"
    EURO3 = "EURO-3"
    EURO4 = "EURO-4"
    EURO5 = "EURO-5"
    EURO6 = "EURO-6"
