import requests
from typing import Optional, Dict, Any
import redis
from app.core.configs.settings import settings


class ProductAPIClient:
    def __init__(self, redis_client: redis.Redis):
        self.base_url = settings.product_api_url
        self.redis = redis_client
        self.cache_ttl = settings.cache_ttl_seconds
        self.timeout = 5

    def _get_cache_key(self, product_id: str) -> str:
        return f"product:exists:{product_id}"

    def _check_cache(self, product_id: str) -> Optional[bool]:
        key = self._get_cache_key(product_id)
        cached = self.redis.get(key)
        if cached is not None:
            return cached == "1"
        return None

    def _cache_product(self, product_id: str, exists: bool) -> None:
        key = self._get_cache_key(product_id)
        value = "1" if exists else "0"
        self.redis.setex(key, self.cache_ttl, value)

    def product_exists(self, product_id: str) -> bool:
        cached_result = self._check_cache(product_id)
        if cached_result is not None:
            return cached_result

        try:
            url = f"{self.base_url}/{product_id}/"
            print(f"url -> {url}")
            response = requests.get(url, timeout=self.timeout)
            print(f"response -> {response}")
            exists = response.status_code == 200

            self._cache_product(product_id, exists)

            return exists

        except requests.Timeout:
            raise ValueError(f"Timeout checking product {product_id}")
        except requests.RequestException as e:
            raise ValueError(f"Error checking product {product_id}: {str(e)}")

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/{product_id}/"
            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            return None

        except requests.RequestException:
            return None
