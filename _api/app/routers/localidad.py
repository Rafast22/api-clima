from fastapi import Depends, APIRouter, status, Body, BackgroundTasks
from typing import Annotated, List
from .._models.user import User
from .._schemas.localidad import RequestLocalidad, RequestLocalidadCreate
from .._view.localidad import (
    update_localidad as update_localidad_view,
    get_localidad_by_id as get_localidad_by_id_view,
    get_localidad_by_cultivo as get_localidad_by_cultivo_view,
    get_localidades_by_user_id as get_localidades_by_user_id_view,
    delete_localidad as delete_localidad_by_id_view,
    create_localidad as create_localidad_view)

from ..database import get_db
from .._view.auth.auth import is_user_autenticate, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/localidad", tags=["Localidad"])

    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_localidad(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                           localidad: RequestLocalidadCreate = Body(...), 
                           db: Session = Depends(get_db),
                            user: User = Depends(get_current_user),
                           background_tasks: BackgroundTasks = BackgroundTasks()):
    
    await create_localidad_view(db, localidad, background_tasks, user)

@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_localidad(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                            localidad: RequestLocalidad = Body(...),  
                            db: Session = Depends(get_db)):
    
    return update_localidad_view(db, localidad)
    
@router.get("/{localidad_id}", response_model=RequestLocalidad)
async def get_localidad_by_id(localidad_id: int, 
                              is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                              db: Session = Depends(get_db)):
    
    return get_localidad_by_id_view(db, localidad_id)

@router.get("/cultivo/{cultivo_id}", response_model=List[RequestLocalidad])
async def get_by_localidad_by_cultivo(cultivo_id: int, 
                                      is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                                      db: Session = Depends(get_db)):
    
    return get_localidad_by_cultivo_view(db, cultivo_id)
    
@router.get("/user/{user_id}", response_model=List[RequestLocalidad])
async def get_localidades_by_user_id(user_id: int, 
                                     is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                                     db: Session = Depends(get_db)):
    
    return get_localidades_by_user_id_view(db, user_id)
    
@router.delete("/{localidad_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_localidad_by_id(localidad_id: int, 
                                 is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                                 db: Session = Depends(get_db)):
    
    delete_localidad_by_id_view(db, localidad_id)

    
    
