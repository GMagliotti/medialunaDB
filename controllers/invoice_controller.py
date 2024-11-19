from fastapi import APIRouter, Depends
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection
from generators import get_mongo_connection, get_cassandra_connection
from models.invoice_dto import InvoiceDTO
from services.invoice_service import InvoiceService

invoice_router = APIRouter()


@invoice_router.get(
    "/{first_name}/{last_name}", response_model=list[InvoiceDTO]
)
async def get_invoices(
        first_name: str,
        last_name: str,
        mongo_client: MongoConnection = Depends(get_mongo_connection),
        cassandra_client: CassandraConnection = Depends(get_cassandra_connection)
):

    invoice_service = InvoiceService(mongo_client, cassandra_client)

    raw_invoices = invoice_service.get_invoices_by_user_name_and_surname(first_name, last_name)
    result = [
        InvoiceDTO.from_model(invoice_data["invoice"], invoice_data["detail"])
        for invoice_data in raw_invoices
    ]

    return result
