from typing import Callable

from openfisca_core.commons import Aggregatable, Array
from openfisca_core.parameters import ParameterNodeAtInstant
from openfisca_core.periods import Instant, Period

#: A callable to get the parameters for the given instant.
Params = Callable[[Instant], ParameterNodeAtInstant]

#: A callable defining a calculation, or a rule, on a system.
Formula = Callable[[Aggregatable, Period, Params], Array]
