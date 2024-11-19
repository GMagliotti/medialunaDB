from fastapi import APIRouter, Depends, status
from typing import List
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection
from generators import get_mongo_connection, get_cassandra_connection
from services.product_service import ProductService
from models.product_dto import ProductDTO
from models.populate.product import Product as ProductServiceModel

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

    result = [conversion_method(product) for product in raw_products]

    return result

@product_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_product(
    product: ProductDTO,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    product_model = ProductServiceModel(
        product_id = product.product_id,
        brand = product.brand,
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock
    )
    product_service = ProductService(mongo_client, cassandra_client)
    product_service.add_product(product_model)
    return {"message": "Product added successfully"}

@product_router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def put_product(
    product_id: int,
    product: ProductDTO,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    product_model = ProductServiceModel(
        product_id = product.product_id,
        brand = product.brand,
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock
    )
    product_service = ProductService(mongo_client, cassandra_client)
    product_service.modify_product(product_model)
    return {"message": "Product modified successfully"}  

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    product_service = ProductService(mongo_client, cassandra_client)
    product_service.delete_product_by_id(product_id)
    return {"message": "Product deleted successfully"}  

@product_router.get("/id-with-invoices", response_model=List[int])
async def get_product_id_with_invoices(
    page: int = 0,
    page_size: int = 0,
    mongo_client: MongoConnection = Depends(get_mongo_connection),
    cassandra_client: CassandraConnection = Depends(get_cassandra_connection),
):
    product_service = ProductService(mongo_client, cassandra_client)

    return product_service.get_product_ids_with_invoices()
