import ftplib
import configparser
from pathlib import Path


def upload_file_to_ftp(file_path: str, cfg_path: str = "ftp.conf") -> str:
    cfg_file = Path(cfg_path)
    if not cfg_file.is_file():
        raise FileNotFoundError(f"Error: '{cfg_path}' does not exist")

    parser = configparser.ConfigParser()
    parser.read(cfg_file, encoding="utf-8")
    if "ftp" not in parser:
        raise KeyError("Error: lack of [ftp] section")

    fp = Path(file_path)
    if not fp.is_file():
        raise FileNotFoundError(file_path)

    host = parser["ftp"]["host"]
    user = parser["ftp"]["user"]
    pwd = parser["ftp"]["password"]
    remote_dir = parser["ftp"].get("remote_dir", "/")

    with ftplib.FTP(host) as ftp:
        ftp.login(user, pwd)
        ftp.cwd(remote_dir)
        with fp.open("rb") as f:
            ftp.storbinary(f"STOR {fp.name}", f)

    return f"{remote_dir.rstrip('/')}/{fp.name}"
