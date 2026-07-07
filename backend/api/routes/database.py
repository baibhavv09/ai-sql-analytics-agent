from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.models import User
from backend.schemas.database import (
    DatabaseConnectionCreate,
    DatabaseConnectionUpdate,
    DatabaseConnectionResponse,
    DatabaseConnectionTest,
)
from backend.services.database_service import DatabaseService
from backend.api.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/database",
    tags=["Database"],
)

database_service = DatabaseService()

@router.post("/test")
def test_database_connection(
    connection: DatabaseConnectionTest,
):

    success, message = database_service.test_connection(
        username=connection.username,
        password=connection.password,
        host=connection.host,
        port=connection.port,
        database_name=connection.database_name,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return {
        "message": message
    }

@router.post(
    "/connect",
    response_model=DatabaseConnectionResponse,
)
def connect_database(
    connection: DatabaseConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return database_service.create_connection(
        db=db,
        user_id=current_user.id,
        connection_data=connection,
    )


@router.get(
    "",
    response_model=DatabaseConnectionResponse,
)
def get_database_connection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    connection = database_service.get_connection(
        db=db,
        user_id=current_user.id,
    )

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Database connection not found",
        )

    return connection


@router.put(
    "",
    response_model=DatabaseConnectionResponse,
)
def update_database_connection(
    connection_data: DatabaseConnectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    connection = database_service.get_connection(
        db=db,
        user_id=current_user.id,
    )

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Database connection not found",
        )

    return database_service.update_connection(
        db=db,
        connection=connection,
        update_data=connection_data,
    )

@router.delete("")
def delete_database_connection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    connection = database_service.get_connection(
        db=db,
        user_id=current_user.id,
    )

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Database connection not found",
        )

    database_service.delete_connection(
        db=db,
        connection=connection,
    )

    return {
        "message": "Database connection deleted successfully"
    }

