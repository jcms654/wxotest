from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date


app = FastAPI()

Listofcustomers = [
    {"id": 1, "firstName": "John", "lastName": "Doe", "accountNumber":"1234567890", "accountType":"Saving",  "phoneNumber": "567438219", "email": "john.doe@example.com", "passportNumber":"65478763", "birthDate":"1988/01/01", "completed": True},
    {"id": 2, "firstName": "Jane", "lastName": "Doe", "accountNumber":"9876543210", "accountType":"Current", "phoneNumber": "870954654", "email": "jane.doe@example.com", "passportNumber":"55437765", "birthDate":"1999/02/02", "completed": False}
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
