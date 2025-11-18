from sqlalchemy import MetaData

def metadata_reflect(engine):
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table_names = list(metadata.tables.keys())
        if table_names:
            first_table_name = list(metadata.tables.keys())[0]
            columns_of_first_table = [column.name for column in metadata.tables[first_table_name].columns]
            return table_names, columns_of_first_table
        return table_names, []
    except Exception as e:
        raise e