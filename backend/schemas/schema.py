from pydantic import BaseModel, Field


class ColumnSchema(BaseModel):
    name: str
    datatype: str
    nullable: bool
    primary_key: bool = False
    foreign_key: bool = False
    indexed: bool = False
    autoincrement: bool = False
    default: str | None = None


class ForeignKeySchema(BaseModel):
    column: str
    referred_table: str
    referred_column: str


class TableSchema(BaseModel):

    name: str
    columns: list[ColumnSchema]
    foreign_keys: list[ForeignKeySchema]
    indexes: list[str] = Field(default_factory=list)


class DatabaseSchema(BaseModel):

    database: str
    tables: list[TableSchema]
    views: list[str] = Field(default_factory=list)