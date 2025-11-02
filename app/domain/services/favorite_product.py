from typing import List
from rq import Queue
from rq.job import Job

from app.domain.schemas.favorite_product import FavoriteProduct
from app.domain.interfaces.favorite_product import IFavoriteProductRepository
from app.infrastructure.tasks.favorite_product_task import (
    create_favorite_task,
    delete_favorite_task,
)
from redis import Redis


class FavoriteProductService:
    def __init__(
        self,
        repository: IFavoriteProductRepository,
        queue: Queue,
        redis_rq: Redis,
    ):
        self.repository = repository
        self.queue = queue
        self.redis_rq = redis_rq

    def get_customer_favorites(
        self, customer_id: int
    ) -> List[FavoriteProduct]:
        return self.repository.get_by_customer(customer_id)

    def get_favorite_by_id(self, favorite_id: int) -> FavoriteProduct:
        favorite = self.repository.get_by_id(favorite_id)
        if not favorite:
            raise ValueError(f"Favorite with id {favorite_id} not found")
        return favorite

    def add_to_favorites_async(self, customer_id: int, product_id: str) -> str:
        job = self.queue.enqueue(
            create_favorite_task,
            customer_id,
            product_id,
            job_timeout="5m",
            result_ttl=86400,
        )
        return job.id

    def remove_from_favorites_async(
        self, customer_id: int, product_id: str
    ) -> str:
        job = self.queue.enqueue(
            delete_favorite_task,
            customer_id,
            product_id,
            job_timeout="5m",
            result_ttl=86400,
        )
        return job.id

    def get_job_status(self, job_id: str) -> dict:
        try:
            job = Job.fetch(job_id, connection=self.redis_rq)

            status_info = {
                "job_id": job.id,
                "status": job.get_status(),
                "created_at": job.created_at.isoformat()
                if job.created_at
                else None,
                "started_at": job.started_at.isoformat()
                if job.started_at
                else None,
                "ended_at": job.ended_at.isoformat() if job.ended_at else None,
            }

            if job.is_finished:
                status_info["result"] = job.result

            if job.is_failed:
                status_info["error"] = str(job.exc_info)

            return status_info

        except Exception as e:
            raise ValueError(f"Job not found: {str(e)}")
