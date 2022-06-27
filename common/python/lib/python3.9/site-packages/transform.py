from typing import Callable
from re import sub

from .enums import NamingConventions

def parse_snake_to_camel(snake_str: str) -> str:
    components = snake_str.lstrip("_").split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def parse_snake_to_pascal(snake_str: str) -> str:
    return snake_str.replace("_", " ").title().replace(" ", "")


def parse_camel_to_snake(camel_str: str) -> str:
    camel_str = sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()


def parse_camel_to_pascal(camel_str: str) -> str:
    return camel_str[0].upper() + camel_str[1:]


def parse_pascal_to_snake(pascal_str: str) -> str:
    return parse_camel_to_snake(pascal_str)


def parse_pascal_to_camel(pascal_str: str) -> str:
    return pascal_str[0].lower() + pascal_str[1:]

class TransformDictionary(object):

    @staticmethod
    def _update_key_names(dictionary: dict, parser: Callable) -> dict:
        updated_dict = dict()
        for key, value in dictionary.items():
            new_key = parser(key)
            if type(value) is dict:
                updated_dict[new_key] = TransformDictionary._update_key_names(value, parser)
            else:
                updated_dict[new_key] = value
        return updated_dict

    """
    This function will iterate over the given dictionary keys and will update them accordingly
    to the given new name convention.

    Parameters:

        - dictionary: dictionary that will be iterated
    
        - current: current name convention in place for the given dictionary keys
    
        - new: new name convention to be applied to the given dictionary keys
    """
    @staticmethod
    def update_naming_convention(dictionary: dict, current: str, new: str) -> dict:
        parser = None

        if current == NamingConventions.SNAKE:
            if new == NamingConventions.CAMEL:
                parser = parse_snake_to_camel
            elif new == NamingConventions.PASCAL:
                parser = parse_snake_to_pascal
        elif current == NamingConventions.CAMEL:
            if new == NamingConventions.SNAKE:
                parser = parse_camel_to_snake
            elif new == NamingConventions.PASCAL:
                parser = parse_camel_to_pascal
        elif current == NamingConventions.PASCAL:
            if new == NamingConventions.SNAKE:
                parser = parse_pascal_to_snake
            elif new == NamingConventions.CAMEL:
                parser = parse_pascal_to_camel

        if parser is None:
            raise ValueError(f"No parser has been found for the naming convention requested: from {current} to {new}.")

        return TransformDictionary._update_key_names(dictionary, parser)
    
