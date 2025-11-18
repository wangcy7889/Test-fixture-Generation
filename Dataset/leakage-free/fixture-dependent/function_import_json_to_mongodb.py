
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError


def import_json_to_mongodb(json_path: str,
                           db_name: str = "testdb",
                           collection: str = "docs") -> int:

    uri = os.getenv("MONGO_URI")
    if not uri:
        raise EnvironmentError("Error: MONGO_URI is not set")

    jp = Path(json_path)
    if not jp.is_file():
        raise FileNotFoundError(f"Error: {json_path} is not a file")

    try:
        data: List[Dict[str, Any]] = json.loads(jp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError("Error: JSON file is not vaild") from e

    if not isinstance(data, list):
        raise ValueError("Error:The top layer of JSON must be an array")

    client = MongoClient(uri)
    try:
        col = client[db_name][collection]
        result = col.insert_many(data)
        return len(result.inserted_ids)
    finally:
        client.close()
