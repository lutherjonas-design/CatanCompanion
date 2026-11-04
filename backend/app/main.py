from fastapi import FastAPI, Depends, HTTPException, APIRouter, Path
from typing import Annotated

from sqlalchemy.orm import Session #type: ignore
from backend.app.db_interaction.db import get_db
from backend.app.db_interaction import crud, schemas
from backend.app.helper.enums import PlayerIncludeParameter
from backend.app.helper.deps import validate_include
from backend.app.setup.setup import populate_initial_data

app = FastAPI(title="Catan Companion API")
router = APIRouter(prefix='/api', tags=["Game"])
#-----------------------------------------------------------------
# Create tables
@app.on_event("startup")
def on_startup():
    db = next(get_db())
    # Create tables
    from backend.app.db_interaction.db import Base, engine
    Base.metadata.create_all(bind=engine)
    # Populate initial data
    populate_initial_data(db)
#-----------------------------------------------------------------
# all about colors
@router.get("/colors/available", response_model=list[str])
def get_available_colors(db: Session = Depends(get_db)):
    return crud.get_available_colors(db)
#All around Player data
@router.get("/players", response_model=list[schemas.Player],
    response_model_exclude_unset=True)
def get_all_players(db: Session = Depends(get_db)):
    return crud.get_all_players(db)

@router.get("/players/{player_id}", response_model=schemas.Player)
def get_player_data(
    player_id: Annotated[int, Path(..., ge=1, description="The ID of the player (>=1) to retrieve")],
    include: Annotated[set[PlayerIncludeParameter], Depends(validate_include)],
    db: Session = Depends(get_db)
):
    try:
        return crud.get_player_data(player_id=player_id, include=include, db=db)
    except crud.NotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")
    except crud.BadIncludeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/players/create", response_model=schemas.Player)
def add_player(payload: schemas.PlayerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_player(db, payload)
    except crud.PlayerNameConflictError:
        raise HTTPException(status_code=409, detail="Player name already exists")
    except crud.PlayerColorConflictError:
        raise HTTPException(status_code=409, detail="Player color already exists")
#-----------------------------------------------------------------
# have a landing page
app.include_router(router)
@app.get("/", tags=["system"])
def health(db: Session = Depends(get_db)):
    return {"status": "ok"}
