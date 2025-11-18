import ree as re

def setPage(url, page):
    url = url.replace('http://', 'https://')
    if re.findall('https://[\\w]*[.]?donmai.us/?$', url):
        url = 'https://{}donmai.us/posts?page=1'.format('danbooru.' if 'danbooru.' in url else '')
    if 'page=' in url:
        url = re.sub('page=[0-9]*', 'page={}'.format(page), url)
    else:
        url += '&page={}'.format(page)
    return url