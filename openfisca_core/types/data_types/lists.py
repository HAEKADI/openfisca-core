from typing import Dict, List, TypeVar, Union


Args = List
T = TypeVar("T", bound = Args)

Roles = List[Dict[str, Union[str, List[str]]]]
