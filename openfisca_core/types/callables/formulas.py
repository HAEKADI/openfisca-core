from typing import Callable

from ..protocols.timeable import Timeable
from ..protocols._aggregatable import Aggregatable
from ..protocols._instantizable import Instantizable
from ..data_types import ArrayType

ParamsType = Callable[[Timeable], Instantizable]
"""A callable to get the parameters for the given instant.

.. versionadded:: 35.7.0

"""

FormulaType = Callable[[Aggregatable, Timeable, ParamsType], ArrayType]
"""A callable defining a calculation, or a rule, on a system.

.. versionadded:: 35.7.0

"""
