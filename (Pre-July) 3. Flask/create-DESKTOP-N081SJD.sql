-- Drop the table 'dbo.flights' in schema 'SchemaName'
IF EXISTS (
    SELECT *
        FROM sys.tables
        JOIN sys.schemas
            ON sys.tables.schema_id = sys.schemas.schema_id
    WHERE sys.schemas.name = N'SchemaName'
        AND sys.tables.name = N'dbo.flights'
)
    DROP TABLE SchemaName.dbo.flights
GO