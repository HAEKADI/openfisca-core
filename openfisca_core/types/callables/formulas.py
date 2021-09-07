from typing import Callable

from openfisca_core.periods import Instant, Period

from ..protocols._aggregatable import Aggregatable
from ..protocols._instantizable import Instantizable
from ..data_types import ArrayType

ParamsType = Callable[[Instant], Instantizable]
"""A callable to get the parameters for the given instant."""

FormulaType = Callable[[Aggregatable, Period, ParamsType], ArrayType]
"""A callable defining a calculation, or a rule, on a system."""
