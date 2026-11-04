from sqlalchemy import Integer, String, JSON, ForeignKey, CheckConstraint,UniqueConstraint, Index #type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship #type: ignore
from typing import Optional

from backend.app.db_interaction.db import Base

# work in progress
class Items(Base):
    __tablename__ = "items"
    # params
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Easier Use
    inventory_entries: Mapped[list["InventoryEntries"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True
    )

class InventoryEntries(Base):
    __tablename__ = "inventory_entries"
    # params
    id: Mapped[int] = mapped_column(Integer,primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # constraints
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='ck_inventory_quantity_nonnegative'),
        UniqueConstraint('player_id', 'item_id', name='uq_inventory_player_item'),
        Index('ix_inventory_player_item', 'player_id', 'item_id'),
    )
    # Easier Use
    player: Mapped["Player"] = relationship(back_populates="inventory_entries")
    item: Mapped["Items"] = relationship(
        back_populates="inventory_entries",
        lazy="selectin",
    )

class Player(Base):
    __tablename__ = "player"
    # params
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    color_hex: Mapped[str] = mapped_column(String(7),nullable=False, default="#FFFFFF")
    # constraints
    __table_args__ = (
        UniqueConstraint('name', name='uq_player_name'),
        UniqueConstraint('color_hex', name='uq_player_color_hex'),
    )
    # Easier Use
    inventory_entries: Mapped[list["InventoryEntries"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
        lazy="selectin",
    )
