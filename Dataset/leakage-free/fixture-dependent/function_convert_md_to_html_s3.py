
import os, markdown, boto3
from pathlib import Path

def convert_md_to_html_s3(md_path: str,
                          bucket: str,
                          key_prefix: str = '',
                          env_region: str = 'AWS_REGION') -> str:

    region = os.getenv(env_region)
    if not region:
        raise EnvironmentError('Error: AWS_REGION is ont set')
    md_file = Path(md_path)
    if not md_file.is_file():
        raise FileNotFoundError(md_path)

    html = markdown.markdown(md_file.read_text(encoding='utf-8'))
    key = f"{key_prefix.rstrip('/')}/{md_file.stem}.html" if key_prefix else md_file.stem+'.html'

    s3 = boto3.client('s3', region_name=region)
    s3.put_object(Bucket=bucket, Key=key, Body=html, ContentType='text/html; charset=utf-8')
    return f's3://{bucket}/{key}'
