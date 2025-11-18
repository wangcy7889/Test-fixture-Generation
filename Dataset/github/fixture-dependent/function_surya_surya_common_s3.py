from pathlib import Path
import requests

def download_file(remote_path: str, local_path: str, chunk_size: int=1024 * 1024):
    local_path = Path(local_path)
    try:
        response = requests.get(remote_path, stream=True, allow_redirects=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        return local_path
    except Exception as e:
        if local_path.exists():
            local_path.unlink()
        print(f'Download error for file {remote_path}: {str(e)}')
        raise