from typing import Dict, List, TypeVar, Union


Args = List
T = TypeVar("T", bound = Args)

Subroles = List[str]

Roles = List[Dict[str, Union[str, Subroles]]]
