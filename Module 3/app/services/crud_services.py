from app.models.item_model import Item
from app.utils.exceptions import ItemNotFoundError
from sqlalchemy.orm import Session


def create_item(db: Session, item: Item) :
    db_item = Item(name=item.name, value=item.value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> Item:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise ItemNotFoundError(f"Item with id {item_id} not found")
    return db_item

def update_item(db: Session, item: Item, item_id) -> Item:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise ItemNotFoundError(f"Item with id {item_id} not found")
    db_item.name = item.name
    db_item.value = item.value
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Item:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise ItemNotFoundError(f"Item with id {item_id} not found")    
    db.delete(db_item)
    db.commit()
    return db_item

def list_items(db: Session) :
    all_items = db.query(Item).all()
    if not all_items:
        raise ItemNotFoundError("No items found")
    return all_items