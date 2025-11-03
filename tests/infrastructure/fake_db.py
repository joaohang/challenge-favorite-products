from typing import Any, Optional, List


class FakeQuery:
    def __init__(self, data: list, model_class: Any):
        self.data = data
        self.model_class = model_class
        self._filters = []
        self._offset_val = 0
        self._limit_val = None

    def filter(self, *args, **kwargs):
        self._filters.extend(args)
        return self

    def offset(self, value: int):
        self._offset_val = value
        return self

    def limit(self, value: int):
        self._limit_val = value
        return self

    def first(self) -> Optional[Any]:
        results = self._apply_filters()
        return results[0] if results else None

    def all(self) -> List[Any]:
        results = self._apply_filters()
        if self._offset_val:
            results = results[self._offset_val :]  # noqa: E203
        if self._limit_val:
            results = results[: self._limit_val]

        return results

    def count(self) -> int:
        return len(self._apply_filters())

    def _apply_filters(self) -> List[Any]:
        if not self._filters:
            return self.data.copy()

        results = []
        for item in self.data:
            match = True
            for filter_expr in self._filters:
                if hasattr(filter_expr, "left") and hasattr(
                    filter_expr, "right"
                ):
                    field = str(filter_expr.left).split(".")[-1]
                    value = filter_expr.right.value

                    if (
                        not hasattr(item, field)
                        or getattr(item, field) != value
                    ):
                        match = False
                        break

            if match:
                results.append(item)

        return results


class FakeDB:
    def __init__(self):
        self.data = {}
        self.id_counter = {}
        self._committed = True

    def query(self, model_class: Any) -> FakeQuery:
        model_name = model_class.__name__
        items = self.data.get(model_name, [])
        return FakeQuery(items, model_class)

    def add(self, instance: Any) -> None:
        model_name = instance.__class__.__name__

        if model_name not in self.data:
            self.data[model_name] = []
            self.id_counter[model_name] = 1

        if not hasattr(instance, "id") or instance.id is None:
            instance.id = self.id_counter[model_name]
            self.id_counter[model_name] += 1

        self.data[model_name].append(instance)
        self._committed = False

    def delete(self, instance: Any) -> None:
        model_name = instance.__class__.__name__
        if model_name in self.data:
            self.data[model_name] = [
                item
                for item in self.data[model_name]
                if item.id != instance.id
            ]
        self._committed = False

    def commit(self) -> None:
        self._committed = True

    def rollback(self) -> None:
        pass

    def refresh(self, instance: Any) -> None:
        pass

    def close(self) -> None:
        pass

    def clear(self) -> None:
        self.data.clear()
        self.id_counter.clear()
        self._committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self.close()


fake_db_instance = FakeDB()


def override_get_db(db_instance=None):
    return db_instance or fake_db_instance
