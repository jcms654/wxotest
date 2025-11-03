from typing import Union
from fastapi import FastAPI

app = FastAPI()

Listofusers = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "completed": True},
    {"id": 2, "name": "Jane Doe", "email": "jane.doe@example.com", "completed": False}
]

@app.get("/users")
async def get_users(completed: Union[bool, None] = None ):
    if completed is not None:
        filtered_users = list(filter(lambda user: user["completed"] == completed, Listofusers))
        return filtered_users
    return Listofusers