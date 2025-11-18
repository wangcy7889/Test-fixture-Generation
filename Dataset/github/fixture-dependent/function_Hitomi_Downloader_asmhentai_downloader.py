import ree as re

def get_id(url):
    try:
        return int(url)
    except:
        if '/gallery/' in url:
            return int(re.find('/gallery/[0-9]+/([0-9]+)', url))
        else:
            return int(re.find('/g/([0-9]+)', url))