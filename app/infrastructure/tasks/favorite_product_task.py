from sqlalchemy.orm import Session
from app.infrastructure.database.postgres import SessionLocal
from app.infrastructure.repositories.favorite_product import (
    FavoriteProductRepository,
)
from app.infrastructure.cache.redis import RedisClient


def create_favorite_task(customer_id: int, product_id: str) -> dict:
    db: Session = SessionLocal()
    redis_client = RedisClient.get_instance()

    try:
        repository = FavoriteProductRepository(db, redis_client)
        favorite = repository.create(customer_id, product_id)

        return {
            "success": True,
            "favorite_id": favorite.id,
            "customer_id": favorite.customer_id,
            "product_id": favorite.product_id,
            "message": "Favorite created successfully",
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
            "customer_id": customer_id,
            "product_id": product_id,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "internal_error",
            "customer_id": customer_id,
            "product_id": product_id,
        }
    finally:
        db.close()


def delete_favorite_task(customer_id: int, product_id: str) -> dict:
    db: Session = SessionLocal()
    redis_client = RedisClient.get_instance()

    try:
        repository = FavoriteProductRepository(db, redis_client)
        success = repository.delete_by_customer_and_product(
            customer_id, product_id
        )

        if success:
            return {
                "success": True,
                "customer_id": customer_id,
                "product_id": product_id,
                "message": "Favorite deleted successfully",
            }
        else:
            return {
                "success": False,
                "error": "Favorite not found",
                "error_type": "not_found",
                "customer_id": customer_id,
                "product_id": product_id,
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "internal_error",
            "customer_id": customer_id,
            "product_id": product_id,
        }
    finally:
        db.close()
