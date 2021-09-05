from typing import Dict, List, TypeVar, Union


Kwds = Dict
T = TypeVar("T", bound = Kwds)

RoleLike = Dict[str, Union[str, List[str]]]
