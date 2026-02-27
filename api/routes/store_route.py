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
@router.get("/{store_ID}/ID",response_model=Store)
def get_id(store_ID: int=Path(...)):
        
    result=getStoreByID(store_ID)
    if result is None:
        raise HTTPException(status_code=404, detail="Store not found")
        
    if result is False:
        raise HTTPException(
        status_code=400,
        detail="Database error")
    return result
    
    #gets a stores by stor_code 
@router.get("/{code}/code",response_model=Store)
def get_store(code: str=Path(...)):
    code=code.strip()
    result= GetBystore_code(code)
    
    if result is False:
         raise HTTPException(status_code=400,
                             detail="Invalid data or database error")
    if result is None:
        raise HTTPException(status_code=404, 
                            detail="Store not found")
    return result
    
@router.post("/addStore",response_model=Store)
def add_store(store:StoreCreate):
    name=str(store.name)
    name=name.strip()
    location=str(store.location)
    location=location.strip()
    status=str(store.status)
    
    val=addStore(name,location,status)
    
    if val is False:
        raise HTTPException(status_code=400,detail="Invalid data or database error")
    if val is None:
        raise HTTPException(status_code=409,detail="Store already exists")
    fullstore=getStoreByID(val)
    if not fullstore:
        raise HTTPException(status_code=500, detail="Error retrieving store")
    return {"store_id": fullstore}

#updates status
@router.put("/{store_id}/status")
def updateStatus(status:statusTable = ...,store_id: int=Path(..., description="ID of the store to update")):#needs a Path?
     
    val=UpdateStoreStatus(store_id,status.value)
    if val:
        return {"message": f"store {store_id} updated to '{status.value}'"}
    raise HTTPException(status_code=400,detail="was not able to update store status")
         
    #http://localhost:8000/docs