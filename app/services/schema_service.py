from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from app.schemas.schema import (
    ColumnSchema,
    DatabaseSchema,
    ForeignKeySchema,
    TableSchema,
)


class SchemaService:

    def __init__(self, engine: Engine):
        self.engine = engine
        self.inspector = inspect(engine)

    def get_tables(self) -> list[str]:
        """
        Return all user tables.
        """
        return self.inspector.get_table_names()

    def get_views(self) -> list[str]:
        """
        Return all database views.
        """
        return self.inspector.get_view_names()

    def get_columns(
        self,
        table_name: str,
    ) -> list[ColumnSchema]:

        columns = []

        db_columns = self.inspector.get_columns(table_name)

        for column in db_columns:

            columns.append(
                ColumnSchema(
                    name=column["name"],
                    datatype=str(column["type"]),
                    nullable=column.get("nullable", True),
                    default=(
                        str(column.get("default"))
                        if column.get("default") is not None
                        else None
                    ),
                    autoincrement=bool(
                        column.get("autoincrement", False)
                    ),
                )
            )

        return columns
    
    def mark_primary_keys(
        self,
        table_name: str,
        columns: list[ColumnSchema],
    ) -> None:
        """
        Mark primary key columns.
        """

        pk_constraint = self.inspector.get_pk_constraint(table_name)

        pk_columns = pk_constraint.get(
            "constrained_columns",
            [],
        )

        for column in columns:

            if column.name in pk_columns:
                column.primary_key = True

    def get_foreign_keys(
        self,
        table_name: str,
        columns: list[ColumnSchema],
    ) -> list[ForeignKeySchema]:
        """
        Return all foreign keys for a table.
        """

        foreign_keys = []

        db_foreign_keys = self.inspector.get_foreign_keys(table_name)

        for fk in db_foreign_keys:

            constrained_columns = fk.get(
                "constrained_columns",
                [],
            )

            referred_columns = fk.get(
                "referred_columns",
                [],
            )

            referred_table = fk.get(
                "referred_table",
            )

            for local_column, remote_column in zip(
                constrained_columns,
                referred_columns,
            ):

                foreign_keys.append(

                    ForeignKeySchema(

                        column=local_column,

                        referred_table=referred_table,

                        referred_column=remote_column,
                    )
                )

                for column in columns:

                    if column.name == local_column:
                        column.foreign_key = True

        return foreign_keys
    
    def get_indexes(
        self,
        table_name: str,
        columns: list[ColumnSchema],
    ) -> list[str]:
        """
        Return indexes for a table and mark indexed columns.
        """

        indexes = []

        db_indexes = self.inspector.get_indexes(table_name)

        for index in db_indexes:

            index_name = index.get("name")

            indexes.append(index_name)

            indexed_columns = index.get(
                "column_names",
                [],
            )

            for column in columns:

                if column.name in indexed_columns:
                    column.indexed = True

        return indexes
    

    def build_table_schema(
        self,
        table_name: str,
    ) -> TableSchema:
        """
        Build complete schema information for a single table.
        """

        # Step 1: Extract all columns
        columns = self.get_columns(table_name)

        # Step 2: Mark primary keys
        self.mark_primary_keys(
            table_name,
            columns,
        )

        # Step 3: Extract foreign keys
        foreign_keys = self.get_foreign_keys(
            table_name,
            columns,
        )

        # Step 4: Extract indexes
        indexes = self.get_indexes(
            table_name,
            columns,
        )

        return TableSchema(
            name=table_name,
            columns=columns,
            foreign_keys=foreign_keys,
            indexes=indexes,
        )
    
    def get_database_schema(
        self,
    ) -> DatabaseSchema:
        """
        Extract the complete database schema.
        """

        tables = []

        for table in self.get_tables():

            tables.append(
                self.build_table_schema(table)
            )

        return DatabaseSchema(
            database=self.engine.url.database,
            tables=tables,
            views=self.get_views(),
        )
    
    def get_schema_prompt(self) -> str:
        """
        Convert the database schema into an LLM-friendly prompt.
        """

        schema = self.get_database_schema()

        lines = []

        lines.append(f"Database: {schema.database}")
        lines.append("")

        for table in schema.tables:

            lines.append(f"Table: {table.name}")

            lines.append("Columns:")

            for column in table.columns:

                info = f"- {column.name} ({column.datatype})"

                flags = []

                if column.primary_key:
                    flags.append("PK")

                if column.foreign_key:
                    flags.append("FK")

                if column.indexed:
                    flags.append("INDEX")

                if column.autoincrement:
                    flags.append("AUTO_INCREMENT")

                if flags:
                    info += " [" + ", ".join(flags) + "]"

                if column.default is not None:
                    info += f" DEFAULT={column.default}"

                lines.append(info)

            if table.foreign_keys:

                lines.append("Relationships:")

                for fk in table.foreign_keys:

                    lines.append(
                        f"- {fk.column} -> "
                        f"{fk.referred_table}.{fk.referred_column}"
                    )

            if table.indexes:

                lines.append("Indexes:")

                for index in table.indexes:

                    lines.append(f"- {index}")

            lines.append("")

        if schema.views:

            lines.append("Views:")

            for view in schema.views:

                lines.append(f"- {view}")

        return "\n".join(lines)