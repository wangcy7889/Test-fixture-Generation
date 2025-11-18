import requests

def get_aws_meta_data() -> dict:
    """ returns aws metadata for current instance

        Returns:
            dict: aws metadata
    """
    aws_meta_data = {'public-hostname': None, 'ami-id': None, 'instance-id': None}
    aws_token = requests.put('http://169.254.169.254/latest/api/token', headers={'X-aws-ec2-metadata-token-ttl-seconds': '30'}).text
    for key in aws_meta_data.keys():
        resp = requests.get(f'http://169.254.169.254/latest/meta-data/{key}', headers={'X-aws-ec2-metadata-token': aws_token}, timeout=1)
        if resp.status_code != 200:
            continue
        aws_meta_data[key] = resp.text
    if aws_meta_data['instance-id'] is None:
        raise Exception('That is not an AWS environment')
    return aws_meta_data