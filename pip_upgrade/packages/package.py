from typing import Any, Self

from packaging.utils import canonicalize_name


class Package:
    def __init__(self, name: str, version: str, location: str, key: str, precedence: int) -> None:
        self.name: str = name
        self.version: str = version
        self.location: str = location
        self.key: str = key
        self.precedence: int = precedence

    def __str__(self) -> str:
        return f"{self.name}=={self.version}"

    def __repr__(self) -> str:
        return f"Package({self.name!r}, {self.version!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Package):
            return NotImplemented
        return self.name == other.name and self.version == other.version

    def __hash__(self) -> int:
        return hash((self.name, self.version))

    @classmethod
    def from_string(cls, string: str) -> Self:
        name, version = string.split("==")
        return cls(name, version)
