import requests
def download_file(url, save_path):
    print(f"Starting download: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    downloaded_size = 0
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                if total_size > 0:
                    progress = (downloaded_size / total_size) * 100
                    print(f"\rDownload progress: {progress:.1f}%", end="", flush=True)
    print(f"\nDownload completed: {save_path}")
