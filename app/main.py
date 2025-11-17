from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

import httpx


app = FastAPI()

Listofcustomers = [
    {"id": 1, "firstName": "John", "lastName": "Doe", "accountNumber":"1234567890", "accountType":"Saving",  "phoneNumber": "567438219", "email": "john.doe@example.com", "passportNumber":"65478763", "birthDate":"1988/01/01", "completed": True},
    {"id": 2, "firstName": "Jane", "lastName": "Doe", "accountNumber":"9876543210", "accountType":"Current", "phoneNumber": "870954654", "email": "jane.doe@example.com", "passportNumber":"55437765", "birthDate":"1999/02/02", "completed": False}
]


orders = [
    {"oc_id": "1005000", "supplier_id": "EN590308934", "oc_date": "2025/08/08", "amount":"198.431,04 ", "oc_status_completed":False, "supplier_name":"Skiles And Sons"},
    {"oc_id": "8029891", "supplier_id": "EN317075017", "oc_date": "2025/07/07", "amount":"18.271,43", "oc_status_completed":False, "supplier_name":"Goodwin-Runolfsson"},
    {"oc_id": "5273598", "supplier_id": "EN610221662", "oc_date": "2023/01/01", "amount":"129.657,67", "oc_status_completed":False, "supplier_name":"Schimmel, Fahey and Morar"},
]     

ordersDetails = [
    {"oc_id": "5273598", "item_id": "J12302", "qty": 1,  "price":"373,71", "qty_pending":1,  "item_description":"Numquam ea et laborum corrupti"}, 
    {"oc_id": "5273598", "item_id": "J12303", "qty": 69, "price":"578,88", "qty_pending":69, "item_description":"Non est non est"},
    {"oc_id": "5273598", "item_id": "J12304", "qty": 97, "price":"572,72", "qty_pending":97, "item_description":"Quia rem esse"},
    {"oc_id": "5273598", "item_id": "J12305", "qty": 23, "price":"691,46", "qty_pending":23, "item_description":"Hic ipsa dolorum"},

    {"oc_id": "8029891", "item_id": "J12306", "qty": 23, "price":"228,27", "qty_pending":23, "item_description":"Provident tempora soluta"},
    {"oc_id": "8029891", "item_id": "J12307", "qty": 16, "price":"647,90", "qty_pending":16, "item_description":"Laudantium laborum nostrum consequatur"},

    {"oc_id": "1005000", "item_id": "J12314", "qty": 62, "price":"892,80", "qty_pending":62, "item_description":"Aut quis placeat omnis"},
    {"oc_id": "1005000", "item_id": "J12315", "qty": 49, "price":"707,09", "qty_pending":49, "item_description":"Aut nam inventore qui"},
    {"oc_id": "1005000", "item_id": "J12316", "qty": 85, "price":"882,85", "qty_pending":85, "item_description":"Qui qui quae"},
    {"oc_id": "1005000", "item_id": "J12317", "qty": 61, "price":"4,39",   "qty_pending":61, "item_description":"Ducimus doloribus quaerat"},
    {"oc_id": "1005000", "item_id": "J12318", "qty": 81, "price":"70,99",  "qty_pending":81, "item_description":"In sunt"},

    
]  

receptions = [
    {"rm_id": 1, "oc_id": "J1234", "rm_date": "2025/01/01", "rm_name":"1234567890"}
]

receptionsDetail = [
    {"rm_id": 1, "item_id": "J1234", "qty": "1"}
]


class Customer(BaseModel):
    firstName: str
    lastName: str
    accountNumber: str
    accountType: str
    phoneNumber: str
    email: str
    passportNumber: str
    birthDate: date
    completed: bool


@app.get("/customers")
async def get_customers(completed: Union[bool, None] = None):
    if completed is not None:
        filtered_customers = list(filter(lambda customer: customer["completed"] == completed, Listofcustomers))
        return filtered_customers
    return Listofcustomers


@app.get("/customer/{customer_id}")
async def get_customer(customer_id: int):
    for customer in Listofcustomers:
        if customer["id"] == customer_id:
            return customer
    return {"error": "Customer not found"}


@app.post("/customer")
async def create_customer(customer: Customer):
    new_id = max(c["id"] for c in Listofcustomers) + 1 if Listofcustomers else 1
    new_customer = customer.dict()
    new_customer["id"] = new_id
    Listofcustomers.append(new_customer)
    return new_customer


@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int):
    for i, customer in enumerate(Listofcustomers):
        if customer["id"] == customer_id:
            deleted = Listofcustomers.pop(i)
            return {"message": "Customer deleted", "customer": deleted}
    return {"error": "Customer not found"}


@app.get("/order/{oc_id}")
async def get_order(oc_id: str):
    # Buscar la orden principal
    order = next((o for o in orders if o["oc_id"] == oc_id), None)
    if not order:
        return {"error": "Order not found"}
    
    # Buscar los detalles asociados
    details = [d for d in ordersDetails if d["oc_id"] == oc_id]
    
    # Combinar la información
    return {
        "order": order,
        "details": details
    }

    
