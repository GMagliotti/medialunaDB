from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.client import Client
from models.client_with_invoice_count import ClientWithInvoiceCount
from models.client_with_total_expenses import ClientWithTotalExpenses
from models.phone import Phone
from models.client_phones_response import ClientPhonesResponse
from models.client_with_phone import PhoneWithClient
from services.client_service import ClientService
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection
from generators import get_mongo_connection, get_cassandra_connection

client_router = APIRouter()


@client_router.get("/", response_model=List[Client])
async def get_clients(
    with_invoices: bool | None = None,
    page: int = 0,
    page_size: int = 0,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    client_service = ClientService(mongo_client, cassandra_client)
    
    clients_m = []
    if with_invoices:
        clients = client_service.get_clients_with_invoices(page=page, page_size=page_size)
        clients_m = list(map(lambda c: Client.from_model(c), clients))
    elif with_invoices is False:
        clients = client_service.get_clients_with_no_invoices(page=page, page_size=page_size)
        clients_m = list(map(lambda c: Client.from_model(c), clients))
    else:
        clients = client_service.get_clients(page=page, page_size=page_size)
        clients_m = list(map(lambda c: Client.from_model(c), clients))

    client_service.end()
    
    return clients_m


@client_router.get(
    "/{first_name}/{last_name}/phones-and-id", response_model=list[ClientPhonesResponse]
)
async def get_client_phones_and_id(
    first_name: str,
    last_name: str,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    client_service = ClientService(mongo_client, cassandra_client)
    clients = client_service.get_clients_by_name(first_name, last_name)

    if not clients:
        raise HTTPException(status_code=404, detail="Client not found")

    response = [
        ClientPhonesResponse(
            client_id=client.client_id,
            phones=[Phone.from_model(phone) for phone in client.phone_list],
        )
        for client in clients
    ]

    return response


@client_router.get("/phones", response_model=List[PhoneWithClient])
async def get_phones_with_client(
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    client_service = ClientService(mongo_client, cassandra_client)
    clients_with_phones = client_service.get_phones_with_client()

    response = [
        PhoneWithClient(
            area_code=client['phone_numbers']['area_code'],
            phone_number=client['phone_numbers']['phone_number'],
            type=client['phone_numbers']['_type'],
            client_id=client['client_id'],
            first_name=client['first_name'],
            last_name=client['last_name'],
            address=client['address'],
            active=client['active']
        )
        for client in clients_with_phones
    ]

    if not response:
        raise HTTPException(status_code=404, detail="No phones with clients found")

    return response

@client_router.get("/with_invoice_count", response_model=List[ClientWithInvoiceCount])
async def get_clients(
    page: int = 0,
    page_size: int = 0,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    client_service = ClientService(mongo_client, cassandra_client)
    
    clients = list(client_service.get_clients_with_invoice_count(page=page, page_size=page_size))
    clients_m = list(map(lambda c: ClientWithInvoiceCount.from_model(c), clients))
    
    client_service.end()
    
    return clients_m

@client_router.get("/with_total_expenses", response_model=List[ClientWithTotalExpenses])
async def get_clients(
    page: int = 0,
    page_size: int = 0,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    client_service = ClientService(mongo_client, cassandra_client)
    
    clients = list(client_service.get_clients_with_total_expenses(page=page, page_size=page_size))
    clients_m = list(map(lambda c: ClientWithTotalExpenses.from_model(c), clients))
        
    return clients_m