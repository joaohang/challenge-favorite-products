from typing import Optional, Union


class FakeRedis:
    def __init__(self):
        self.data = {}

    def get(self, key: Union[str, bytes]) -> Optional[bytes]:
        if isinstance(key, str):
            key = key.encode("utf-8")

        value = self.data.get(key)
        return value

    def set(
        self,
        key: Union[str, bytes],
        value: Union[str, bytes],
        ex: Optional[int] = None,
        nx: bool = False,
    ) -> bool:
        if isinstance(key, str):
            key = key.encode("utf-8")
        if isinstance(value, str):
            value = value.encode("utf-8")

        if nx and key in self.data:
            return False

        self.data[key] = value
        return True

    def setex(
        self, key: Union[str, bytes], time: int, value: Union[str, bytes]
    ) -> bool:
        return self.set(key, value, ex=time)

    def setnx(self, key: Union[str, bytes], value: Union[str, bytes]) -> bool:
        return self.set(key, value, nx=True)

    def getex(
        self,
        key: Union[str, bytes],
        ex: Optional[int] = None,
        px: Optional[int] = None,
    ) -> Optional[bytes]:
        return self.get(key)

    def getset(
        self, key: Union[str, bytes], value: Union[str, bytes]
    ) -> Optional[bytes]:
        old_value = self.get(key)
        self.set(key, value)
        return old_value

    def delete(self, *keys: Union[str, bytes]) -> int:
        count = 0
        for key in keys:
            if isinstance(key, str):
                key = key.encode("utf-8")

            if key in self.data:
                del self.data[key]
                count += 1

        return count

    def exists(self, *keys: Union[str, bytes]) -> int:
        count = 0
        for key in keys:
            if isinstance(key, str):
                key = key.encode("utf-8")

            if key in self.data:
                count += 1

        return count

    def clear(self):
        self.data.clear()

    def keys(self, pattern: str = "*") -> list:
        if pattern == "*":
            return list(self.data.keys())

        return list(self.data.keys())

    def ttl(self, key: Union[str, bytes]) -> int:
        if isinstance(key, str):
            key = key.encode("utf-8")

        return -1 if key in self.data else -2

    def expire(self, key: Union[str, bytes], seconds: int) -> int:
        if isinstance(key, str):
            key = key.encode("utf-8")

        return 1 if key in self.data else 0

    def __repr__(self):
        return f"FakeRedis(keys={len(self.data)})"


fake_redis_client = FakeRedis()


def override_get_redis():
    return fake_redis_client
