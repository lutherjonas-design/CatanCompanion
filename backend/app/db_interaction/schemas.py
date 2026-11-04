from pydantic import BaseModel, ConfigDict
from backend.app.helper.enums import AllowedColors
# Basis-Player-Schema
class PlayerBase(BaseModel):
    name: str
    color_hex: AllowedColors

# Create-Player-Schema
class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Full Player Data Schema
# Inventory Entry Schema
class InventoryEntry(BaseModel):
    item_id: int
    quantity: int

# complete Player Data Schema
class PlayerData(Player):
    inventory: list[InventoryEntry] | None = None