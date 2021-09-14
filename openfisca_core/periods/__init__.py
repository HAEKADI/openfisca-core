# Transitional imports to ensure non-breaking changes.
# Could be deprecated in the next major release.
#
# How imports are being used today:
#
#   >>> from openfisca_core.module import symbol
#
# The previous example provokes cyclic dependency problems
# that prevent us from modularizing the different components
# of the library so to make them easier to test and to maintain.
#
# How could them be used after the next major release:
#
#   >>> from openfisca_core import module
#   >>> module.symbol()
#
# And for classes:
#
#   >>> from openfisca_core.module import Symbol
#   >>> Symbol()
#
# See: https://www.python.org/dev/peps/pep-0008/#imports

from .config import (  # noqa: F401
    DAY,
    MONTH,
    YEAR,
    ETERNITY,
    )

from .config import (  # noqa: F401
    INSTANT_PATTERN,
    YEAR_OR_MONTH_OR_DAY_RE,
    )

from .config import (  # noqa: F401
    STR_BY_INSTANT_CACHE,
    DATE_BY_INSTANT_CACHE,
    )

from .helpers import (  # noqa: F401
    N_,
    instant,
    instant_date,
    key_period_size,
    period,
    unit_weight,
    unit_weights,
    )

from .instant_ import Instant  # noqa: F401
from .period_ import Period  # noqa: F401
from .unit import Unit  # noqa: F401

# For backwards compatibility

str_by_instant_cache = STR_BY_INSTANT_CACHE
date_by_instant_cache = DATE_BY_INSTANT_CACHE
year_or_month_or_day_re = YEAR_OR_MONTH_OR_DAY_RE
