from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class IProductAPI(ABC):
    @abstractmethod
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_products_batch(
        self, product_ids: List[str]
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        pass
