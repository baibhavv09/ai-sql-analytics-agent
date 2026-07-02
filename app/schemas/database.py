from pydantic import BaseModel, Field
from typing import Optional


class DatabaseConnectionCreate(BaseModel):
    connection_name: str = Field(..., min_length=1, max_length=100)
    host: str
    port: int = 3306
    database_name: str
    username: str
    password: str
    db_type: str = "mysql"


class DatabaseConnectionUpdate(BaseModel):
    connection_name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class DatabaseConnectionResponse(BaseModel):
    id: int
    connection_name: str
    db_type: str
    host: str
    port: int
    database_name: str
    username: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class DatabaseConnectionTest(BaseModel):
    host: str
    port: int = 3306
    database_name: str
    username: str
    password: str