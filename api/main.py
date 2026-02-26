import sys
import os
import logging
import psycopg2
from fastapi import FastAPI
from .routes.store_route import router as store_router
from psycopg2.extras import RealDictCursor
from .services.store import getStoreByID
from .data.conect import get_connection
from .routes.models.store_models import Store


#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Inventory API")
app.include_router(store_router)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
@app.get("/")
def home():
    return {"message":"Welcome to the Inventory API its a work in progress."}

        
        #conn=psycopg2.connect( dbname="datastore",user="postgres",password="12345",host="localhost",port="5433")
    
        #uvicorn api.main:app --reload

   
