from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    database_connection = relationship(
        "DatabaseConnection",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class DatabaseConnection(Base):
    __tablename__ = "database_connections"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    connection_name = Column(String(100), nullable=False)

    db_type = Column(String(20), nullable=False, default="mysql")

    host = Column(String(255), nullable=False)

    port = Column(Integer, default=3306)

    database_name = Column(String(255), nullable=False)

    username = Column(String(255), nullable=False)

    encrypted_password = Column(Text, nullable=False)

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="database_connection"
    )