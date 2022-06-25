from enum import EnumMeta, Enum

class CustomEnumMeta(EnumMeta):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value
        return False

    def __contains__(self, other):
        try:
            self(other)
        except ValueError:
            return False
        else:
            return True

class NamingConventions(Enum, metaclass=CustomEnumMeta):
    SNAKE = "snake_case"
    CAMEL = "camelCase"
    PASCAL = "PascalCase"