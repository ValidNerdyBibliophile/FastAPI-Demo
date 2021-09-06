from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name:str
    price:int
    brand:Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price:Optional[int] = None
    brand:Optional[str] = None


app = FastAPI()


'''@app.get("/")
def home():
    return {"Date": "Testing"}


@app.get("/about")
def about():
    return {"Data":"About"}'''



'''inventory = {
    1: {
    "name": "Eggs",
    "price" : "50",
    "brand" : "Organic Tastes"
    }
}'''

inventory = {}

@app.get("/get_item/{item_id}")
def get_item(item_id: int = Path(None,description = "The ID of the item you would like to view.", gt = 0)):
    return inventory[item_id]


'''@app.get("/get_by_name")
def get_item(name: Optional[str] = None, test:int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not Found"}'''



@app.get("/get_by_name")
def get_item(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        #if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/create_item")
def create_item(item_id:int , item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item Already Exists")

    #inventory[item_id] = {"name":item.name, "brand":item.brand, "price":item.price}
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update_item/{item_id}")
def update_item(item_id: int, item:UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item Name Not Found")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete_item")
def delete_item(item_id: int = Query(..., description = "The Id of The item to delete", gt = 0)):
    if item not in inventory:
        return {"Error":"ID does not Exists"}
    del inventory[item_id]
    #return {"SUCESS":"ITEM DELETED"}
    raise HTTPException(status_code=404, detail="Item Name Not Found")
