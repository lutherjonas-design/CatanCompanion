from sqlalchemy.orm import Session #type: ignore
from backend.app.helper.exceptions import NotFoundError, PlayerNameConflictError, PlayerColorConflictError
from backend.app.db_interaction import models, schemas
from backend.app.helper.enums import AllowedColors
# ---------------- Item ----------------
def get_all_items(db: Session):
    return db.query(models.Items).all()
def create_item(db: Session, item_data: dict):
    db_item = models.Items(
        key=item_data["key"],
        name=item_data["name"],
        type=item_data["type"],
        meta=item_data.get("meta", None)
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ---------------- color ----------------
def get_taken_colors(db: Session) -> set[str]:
    return {c[0] for c in db.query(models.Player.color_hex).all()}

def get_available_colors(db: Session) -> list[str]:
    taken = get_taken_colors(db)
    return [c.value for c in AllowedColors if c.value not in taken]

# ---------------- Player ---------------
def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_player_data(player_id: int, include, db: Session):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise NotFoundError()
    inventory_list = None
    if "inventory" in include:
        # Load relationship (lazy load)
        entries = player.inventory_entries
        inventory_list = [
            schemas.InventoryEntry(item_id=e.item_id, quantity=e.quantity)
            for e in entries
        ]
    # Build expanded schema
    return schemas.PlayerData(
        id=player.id,
        name=player.name,
        color_hex=player.color_hex,
        inventory=inventory_list
    )

def create_player(db: Session, payload: schemas.PlayerCreate):  
    if db.query(models.Player).filter(models.Player.name == payload.name).first():
        raise PlayerNameConflictError(f"Player with name '{payload.name}' already exists.")
    if db.query(models.Player).filter(models.Player.color_hex == payload.color_hex).first():
        raise PlayerColorConflictError(f"Player with color '{payload.color_hex}' already exists.")
    db_player = models.Player(name=payload.name,color_hex=payload.color_hex)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

# ---------------- Inventory Entries ---------------
def get_inventory_for_player(player_id: int, db: Session):
    return db.querry(models.InventoryEntries).filter(
        models.InventoryEntries.player_id == player_id
    ).all()

def get_inventory_entry(player_id: int, item_id: int, db: Session):
    entry = db.query(models.InventoryEntries).filter(
        models.InventoryEntries.player_id == player_id,
        models.InventoryEntries.item_id == item_id
    ).first()
    if not entry:
        raise NotFoundError()
    return entry

def create_or_update_inventory_entry(player_id: int, item_id: int, quantity: int, db: Session):
    entry = db.query(models.InventoryEntries).filter(
        models.InventoryEntries.player_id == player_id,
        models.InventoryEntries.item_id == item_id
    ).first()
    if entry:
        entry.quantity = quantity
    else:
        entry = models.InventoryEntries(
            player_id=player_id,
            item_id=item_id,
            quantity=quantity
        )
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry