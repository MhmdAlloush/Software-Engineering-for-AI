# CRUD: Create, Read, Update, Delete
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.item_schema import ItemSchema as Item
from app.services.crud_services import create_item, get_item, update_item, delete_item, list_items
from app.utils.exceptions import ItemNotFoundError
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.database import Base, engine
router = APIRouter(prefix="/items", tags=["items"])

# POST locahost:8000/items
Base.metadata.create_all(bind=engine)

@router.post("/add_item", response_model=Item)
def add_item_route(item: Item, db: Session = Depends(get_db)):
    """
    Create a new item.
    """
    return create_item(db, item)


@router.get("/get_item", response_model=Item)
def get_item_route(item_id: int, db:Session = Depends(get_db)):
    """
    Get an item by its ID.
    """
    try:
        return get_item(db,item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.put("/update_item", response_model=Item)
def update_item_route(item_id,item: Item, db:Session = Depends(get_db)):
    """
    Update an existing item by its ID.
    """
    try:
        return update_item(db, item, item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/delete_item", response_model=Item)
def delete_item_route(item_id: int):
    """
    Delete an item by its ID.
    """
    try:
        return delete_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/", response_model=list[Item])
def list_items_route(db: Session = Depends(get_db)):
    """
    List all items.
    """
    items = list_items(db)
    all_items_schema = []
    for item in items:
        item_schema=Item(id=item.id,name=item.name,value=item.value)
        all_items_schema.append(item_schema)
    return all_items_schema