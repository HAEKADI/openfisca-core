from typing import Callable

from openfisca_core.periods import Instant, Period

from ..protocols import Aggregatable, Instantizable
from ..data_types import Array

#: A callable to get the parameters for the given instant.
Params = Callable[[Instant], Instantizable]

#: A callable defining a calculation, or a rule, on a system.
Formula = Callable[[Aggregatable, Period, Params], Array]
