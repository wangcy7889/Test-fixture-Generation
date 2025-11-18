
import os
from ftplib import FTP
from pathlib import Path

def ftp_upload_file(file_path: str,
                    remote_dir: str = '/',
                    env_host: str = 'FTP_HOST',
                    env_user: str = 'FTP_USER',
                    env_pass: str = 'FTP_PASS') -> str:
    host = os.getenv(env_host); user = os.getenv(env_user); pw = os.getenv(env_pass)
    if not all([host, user, pw]):
        raise EnvironmentError('Error: FTP Environment variables not set')
    fp = Path(file_path)
    if not fp.is_file():
        raise FileNotFoundError(f"Error: '{file_path}' is not found")
    with FTP(host) as ftp:
        ftp.login(user, pw)
        ftp.cwd(remote_dir)
        with fp.open('rb') as f:
            ftp.storbinary(f'STOR {fp.name}', f)
    return f'ftp://{host}{remote_dir}/{fp.name}'
