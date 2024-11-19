from fastapi import APIRouter, Depends
from typing import List
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection
from generators import get_mongo_connection, get_cassandra_connection
from services.product_service import ProductService
from models.product_dto import ProductDTO

product_router = APIRouter()


@product_router.get("/", response_model=List[ProductDTO])
async def get_products(
        with_invoices: bool | None = None,
        page: int = 0,
        page_size: int = 0,
        mongo_client: MongoConnection = Depends(get_mongo_connection),
        cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    product_service = ProductService(mongo_client, cassandra_client)

    def fetch_products(with_invoices: bool | None):
        if with_invoices:
            return product_service.get_products_with_invoices(), ProductDTO.from_dict
        elif with_invoices is False:
            return product_service.get_products_with_no_invoice(), ProductDTO.from_dict
        else:
            return product_service.get_products(), ProductDTO.from_model

    raw_products, conversion_method = fetch_products(with_invoices)

    result = [
        conversion_method(product)
        for product in raw_products
    ]

    return result
