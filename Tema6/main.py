#Для запуска введи в консоли uvicorn main:app --reload


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(title="My Simple API", description="An API for managing a list of items.")


db_items: List[Dict[str, Any]] = [
    {"id": 1, "name": "Ноутбук", "description": "Мощный ноутбук для работы"},
    {"id": 2, "name": "Мышь", "description": "Беспроводная оптическая мышь"},
    {"id": 3, "name": "Клавиатура", "description": None},
]

class Item(BaseModel):
    name: str
    description: Optional[str] = None


@app.get("/items", summary="Получить все элементы")
def get_all_items():
    return {"data": db_items}

@app.get("/items/{item_id}", summary="Получить элемент по ID")
def get_item_by_id(item_id: int):
    for item in db_items:
        if item["id"] == item_id:
            return {"data": item}
    raise HTTPException(status_code=404, detail=f"Элемент с id={item_id} не найден")

@app.post("/items", status_code=201, summary="Создать новый элемент")
def create_item(item: Item):
    new_id = max(i["id"] for i in db_items) + 1 if db_items else 1

    new_item = {
        "id": new_id,
        "name": item.name,
        "description": item.description
    }

    db_items.append(new_item)

    return {"message": "Элемент успешно создан", "data": new_item}

@app.put("/items/{item_id}", summary="Обновить элемент по ID")
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db_items):
        if item["id"] == item_id:
            db_items[index]["name"] = updated_item.name
            db_items[index]["description"] = updated_item.description
            return {"message": f"Элемент с id={item_id} обновлен", "data": db_items[index]}

    raise HTTPException(status_code=404, detail=f"Элемент с id={item_id} не найден для обновления")

@app.delete("/items/{item_id}", summary="Удалить элемент по ID")
def delete_item(item_id: int):
    global db_items

    item_to_delete = None
    for item in db_items:
        if item["id"] == item_id:
            item_to_delete = item
            break

    if item_to_delete:
        db_items.remove(item_to_delete)
        return {"message": f"Элемент с id={item_id} успешно удален"}

    raise HTTPException(status_code=404, detail=f"Элемент с id={item_id} не найден для удаления")

