from fastapi import APIRouter, Depends
from typing import List
from models.client import Client
from models.phone import Phone
from services.client_service import ClientService
from persistence.mongo_connection import MongoConnection
from generators import get_mongo_connection

client_router = APIRouter()


@client_router.get("/", response_model=List[Client])
async def get_clients(mongo_client: MongoConnection = Depends(get_mongo_connection)):
    client_service = ClientService(mongo_client)
    return client_service.get_clients()


@client_router.get("/{first_name}/{last_name}/phones", response_model=List[Phone])
async def get_client_phones(first_name: str, last_name: str, mongo_client: MongoConnection = Depends(get_mongo_connection)):
    client_service = ClientService(mongo_client)
    return client_service.get_client_by_name(first_name, last_name)

