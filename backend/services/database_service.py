from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from backend.schemas.database import DatabaseConnectionCreate, DatabaseConnectionUpdate
from backend.db.models import DatabaseConnection
from backend.core.config import settings



class DatabaseService:

    def __init__(self):
        self.cipher = Fernet(settings.DATABASE_SECRET_KEY.encode())
    
    def encrypt_password(self, password: str) -> str:
        return self.cipher.encrypt(password.encode()).decode()  
    
    def decrypt_password(self, encrypted_password: str) -> str:
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    def build_connection_url(
    self,
    username: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
    ) -> str:

        return (
            f"mysql+pymysql://"
            f"{username}:{password}@"
            f"{host}:{port}/"
            f"{database_name}"
        )
    
    def test_connection(
    self,
    username: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
    ):

        url = self.build_connection_url(
            username,
            password,
            host,
            port,
            database_name,
        )

        try:

            engine = create_engine(url)

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return True, "Connection successful"

        except SQLAlchemyError as e:

            return False, str(e)
        
    


    def create_connection(
        self,
        db: Session,
        user_id: int,
        connection_data: DatabaseConnectionCreate,
    ):
        """
        Create or update a user's database connection.
        """

        existing = (
            db.query(DatabaseConnection)
            .filter(DatabaseConnection.user_id == user_id)
            .first()
        )

        encrypted_password = self.encrypt_password(
            connection_data.password
        )

        if existing:

            existing.connection_name = connection_data.connection_name
            existing.db_type = connection_data.db_type
            existing.host = connection_data.host
            existing.port = connection_data.port
            existing.database_name = connection_data.database_name
            existing.username = connection_data.username
            existing.encrypted_password = encrypted_password
            existing.is_verified = True

            db.commit()
            db.refresh(existing)

            return existing

        connection = DatabaseConnection(
            user_id=user_id,
            connection_name=connection_data.connection_name,
            db_type=connection_data.db_type,
            host=connection_data.host,
            port=connection_data.port,
            database_name=connection_data.database_name,
            username=connection_data.username,
            encrypted_password=encrypted_password,
            is_verified=True,
        )

        db.add(connection)
        db.commit()
        db.refresh(connection)

        return connection
    
    def get_connection(
        self,
        db: Session,
        user_id: int,
    ):

        return (
            db.query(DatabaseConnection)
            .filter(DatabaseConnection.user_id == user_id)
            .first()
        )

    def get_connection_by_user_id(
        self,
        user_id: int,
    ):
        """
        Session-less lookup used by AI tools that don't receive a db dependency.
        """

        from backend.db.database import SessionLocal

        db = SessionLocal()
        try:
            return self.get_connection(db=db, user_id=user_id)
        finally:
            db.close()
    
    


    def update_connection(
        self,
        db: Session,
        connection: DatabaseConnection,
        update_data: DatabaseConnectionUpdate,
    ):

        data = update_data.model_dump(exclude_unset=True)

        if "password" in data:
            data["encrypted_password"] = self.encrypt_password(
                data.pop("password")
            )

        for key, value in data.items():
            setattr(connection, key, value)

        connection.is_verified = False

        db.commit()
        db.refresh(connection)

        return connection
    
    def delete_connection(
        self,
        db: Session,
        connection: DatabaseConnection,
    ):

        db.delete(connection)
        db.commit()

    def verify_connection(
        self,
        db: Session,
        connection: DatabaseConnection,
    ):

        password = self.decrypt_password(
            connection.encrypted_password
        )

        success, message = self.test_connection(
            username=connection.username,
            password=password,
            host=connection.host,
            port=connection.port,
            database_name=connection.database_name,
        )

        if success:
            connection.is_verified = True
            db.commit()

        return success, message
    
    def get_engine_for_user(
        self,
        connection: DatabaseConnection,
    ):

        password = self.decrypt_password(
            connection.encrypted_password
        )

        url = self.build_connection_url(
            username=connection.username,
            password=password,
            host=connection.host,
            port=connection.port,
            database_name=connection.database_name,
        )

        return create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600,
        )


database_service = DatabaseService()