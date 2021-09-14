from typing import Tuple, Union

from typing_extensions import Literal

# Date unit types.

DayLitl = Literal["DAY", "Day", "day"]
DayType = Tuple[DayLitl, int]
DayLike = Union[DayLitl, DayType]

MonthLitl = Literal["Month", "Month", "month"]
MonthType = Tuple[MonthLitl, int]
MonthLike = Union[MonthLitl, MonthType]

YearLitl = Literal["YEAR", "Year", "year"]
YearType = Tuple[YearLitl, int]
YearLike = Union[YearLitl, YearType]

EternityLitl = Literal["ETERNITY", "Eternity", "eternity"]
EternityType = Tuple[EternityLitl, int]
EternityLike = Union[EternityLitl, EternityType]

EtherealLitl = Union[DayLitl, MonthLitl, YearLitl]
EtherealType = Tuple[DayType, MonthType, YearType]
EtherealLike = Union[DayLike, MonthLike, YearLike]

EternalLitl = Union[EternityLitl]
EternalType = Tuple[EternityType]
EternalLike = Union[EternityLike]

UnitLitl = Union[DayLitl, MonthLitl, YearLitl, EternityLitl]
UnitType = Tuple[DayType, MonthType, YearType, EternityType]
UnitLike = Union[DayLike, MonthLike, YearLike, EternityLike]
