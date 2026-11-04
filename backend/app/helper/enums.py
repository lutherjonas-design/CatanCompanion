from enum import Enum

class PlayerIncludeParameter(str, Enum):
    inventory = "inventory"

class AllowedColors(str, Enum):
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"
    YELLOW = "#FFFF00"
