
import os
from pymongo import MongoClient

def mongo_create_ttl(collection: str,
                     field: str,
                     expire_seconds: int,
                     env_uri: str = 'MONGO_URI') -> str:
    uri=os.getenv(env_uri)
    if not uri:
        raise EnvironmentError('Error: MONGO_URI is not set')
    client=MongoClient(uri)
    try:
        col=client.get_default_database()[collection]
        idx=col.create_index([(field,1)], expireAfterSeconds=expire_seconds, name=f'{field}_ttl')
    finally:
        client.close()
    return idx
