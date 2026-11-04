from backend.app.db_interaction import crud
from backend.app.setup.setup_items import BASE_ITEMS

# Populate the database with initial data if not already present.
def populate_initial_data(db):
    existing_items = crud.get_all_items(db)
    for item in BASE_ITEMS:
        if not (item in existing_items):
            crud.create_item(db, item)