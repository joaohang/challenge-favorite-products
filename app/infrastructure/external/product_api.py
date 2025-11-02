import requests
import json
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import redis
from app.core.configs.settings import settings
from app.domain.interfaces.product_api import IProductAPI


class ProductAPI(IProductAPI):
    def __init__(self, redis_client: redis.Redis):
        self.base_url = settings.product_api_url
        self.redis = redis_client
        self.cache_ttl = settings.cache_ttl_seconds
        self.timeout = settings.api_timeout_seconds
        self.max_concurrent_requests = settings.max_concurrent_requests

    def _get_product_cache_key(self, product_id: str) -> str:
        return f"product:data:{product_id}"

    def _get_cached_product_data(
        self, product_id: str
    ) -> Optional[Dict[str, Any]]:
        key = self._get_product_cache_key(product_id)
        cached = self.redis.get(key)
        if cached:
            cached_str = str(cached) if not isinstance(cached, str) else cached
            return json.loads(cached_str)  # type: ignore[no-any-return]
        return None

    def _cache_product_data(
        self, product_id: str, data: Optional[Dict[str, Any]]
    ) -> None:
        key = self._get_product_cache_key(product_id)
        if data is None:
            self.redis.setex(key, self.cache_ttl, "")
        else:
            self.redis.setex(key, self.cache_ttl, json.dumps(data))

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        key = self._get_product_cache_key(product_id)
        cached = self.redis.get(key)

        if cached is not None:
            if cached == "":
                return None
            cached_str = str(cached) if not isinstance(cached, str) else cached
            return json.loads(cached_str)  # type: ignore[no-any-return]

        try:
            url = f"{self.base_url}/{product_id}/"
            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()

                if "id" in data:
                    data["id"] = str(data["id"])

                self._cache_product_data(product_id, data)
                return data  # type: ignore[no-any-return]

            self._cache_product_data(product_id, None)
            return None

        except requests.RequestException:
            return None

    def _fetch_single_product(
        self, product_id: str
    ) -> tuple[str, Optional[Dict[str, Any]]]:
        data = self.get_product(product_id)
        return product_id, data

    def get_products_batch(
        self, product_ids: List[str]
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        results: Dict[str, Optional[Dict[str, Any]]] = {}

        with ThreadPoolExecutor(
            max_workers=self.max_concurrent_requests
        ) as executor:
            future_to_id = {
                executor.submit(
                    self._fetch_single_product, product_id
                ): product_id
                for product_id in product_ids
            }

            for future in as_completed(future_to_id):
                product_id, data = future.result()
                results[product_id] = data

        return results
