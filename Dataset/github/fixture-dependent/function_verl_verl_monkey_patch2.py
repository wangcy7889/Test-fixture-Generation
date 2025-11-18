import importlib.metadata
from packaging import version

def is_transformers_version_in_range(min_version: str, max_version: str) -> bool:
    try:
        transformers_version = importlib.metadata.version('transformers')
    except importlib.metadata.PackageNotFoundError as e:
        raise ModuleNotFoundError('The `transformers` package is not installed.') from e
    return version.parse(min_version) <= version.parse(transformers_version) <= version.parse(max_version)