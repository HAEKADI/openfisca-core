from typing import Callable

from openfisca_core.periods import Instant, Period

from ..protocols import Aggregatable, Instantizable
from ..data_types import ArrayType

#: A callable to get the parameters for the given instant.
ParamsType = Callable[[Instant], Instantizable]

#: A callable defining a calculation, or a rule, on a system.
FormulaType = Callable[[Aggregatable, Period, ParamsType], ArrayType]
