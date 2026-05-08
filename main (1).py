from fastapi import FastAPI, HTTPException, Query, Path
from typing import Dict, Any, Optional, List

app = FastAPI(title="FastAPI Minimal Lab")

# Хранилище в памяти: { id: { ...поля } }
items: Dict[int, Dict[str, Any]] = {}
next_id = 1


# ── Проверка данных ──────────────────────────────────────────────────────────

def validate_item(data: Dict[str, Any]):
    """Проверяем что name и price переданы корректно."""
    if not isinstance(data, dict):
        raise HTTPException(400, "Body must be a JSON object")

    if "name" not in data or not isinstance(data["name"], str) or len(data["name"].strip()) < 2:
        raise HTTPException(400, "Invalid or missing 'name'")

    if "price" not in data or not isinstance(data["price"], (int, float)) or data["price"] < 0:
        raise HTTPException(400, "Invalid or missing 'price'")

    if "category" in data and not isinstance(data["category"], str):
        raise HTTPException(400, "'category' must be a string")


# ── Эндпоинты ────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items(
    q: Optional[str] = Query(None, description="Поиск по name и description"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    offset: int = 0,
    limit: int = 50,
):
    """Вернуть список товаров с фильтрацией по тексту и категории."""
    data = list(items.values())

    # фильтр по тексту
    if q:
        ql = q.lower()
        data = [i for i in data if ql in i["name"].lower()
                                or ql in str(i.get("description", "")).lower()]

    # фильтр по категории (добавлено по заданию)
    if category:
        data = [i for i in data if i.get("category", "other").lower() == category.lower()]

    return data[offset : offset + limit]


@app.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1)):
    """Получить один товар по ID."""
    item = items.get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@app.post("/items", status_code=201)
def create_item(payload: Dict[str, Any]):
    """Создать товар. Обязательные поля: name, price. Опционально: description, category, in_stock."""
    global next_id
    validate_item(payload)

    payload.setdefault("description", None)
    payload.setdefault("in_stock", True)
    payload.setdefault("category", "other")   # ← новое поле, по умолчанию "other"

    item = {"id": next_id, **payload}
    items[next_id] = item
    next_id += 1
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, payload: Dict[str, Any]):
    """Полностью обновить товар (старые поля сохраняются, новые перезаписывают)."""
    current = items.get(item_id)
    if not current:
        raise HTTPException(404, "Item not found")

    merged = {**current, **payload}
    validate_item(merged)
    items[item_id] = merged
    return merged


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Удалить товар. Возвращает 204 No Content."""
    if item_id not in items:
        raise HTTPException(404, "Item not found")
    del items[item_id]
    return None
