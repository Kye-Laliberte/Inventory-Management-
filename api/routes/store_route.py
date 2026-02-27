from fastapi import APIRouter, HTTPException,Query,Path
from .models.store_models import Store,statusTable,StoreCreate
from ..data.conect import get_connection
from ..services.store import  getStoreByID,GetBystore_code,UpdateStoreStatus,addStore
from psycopg2.extras import RealDictCursor

router=APIRouter(prefix="/store",tags=["store"])

@router.get("/")
def storehome():
    return {"message":"Welcome to the store home page."}
       #get store by ID 
@router.get("/{store_ID}/ID")
def get_id(id: int=Path(...)):
        
    result=getStoreByID(store_id=id)
    if result is None:
        raise HTTPException(status_code=404, detail="Store not found")
        
    if result is False:
        raise HTTPException(
        status_code=400,
        detail="Database error")
    return result
    
    #gets a stores by stor_code 
@router.get("/{store_code}/code")
def get_store(code: str=Path(...)):
    result= GetBystore_code(code)
    if result is False:
         raise HTTPException(status_code=400,
                             detail="Invalid data or database error")
    if result is None:
        raise HTTPException(status_code=404, 
                            detail="Store not found")
    return result
    
@router.post("/addStore",response_model=StoreCreate)
def add_store(store:StoreCreate):
    val=addStore(
         name=store.name,
        location=store.location,
        status=store.status)
    if val is False:
        raise HTTPException(status_code=400,detail="Invalid data or database error")
        
    if val is None:
        raise HTTPException(status_code=409,detail="Store already exists")
    
    return {"store_id": val}

#updates status
@router.put("/{store_id}/status")
def updateStatus(status:statusTable = ...,store_id: int=Path(..., description="ID of the store to update")):#needs a Path?
     
    val=UpdateStoreStatus(store_id,status.value)
    if val:
        return {"message": f"store {store_id} updated to '{status.value}'"}
    raise HTTPException(status_code=400,detail="was not able to update store status")
         
    #http://localhost:8000/docs