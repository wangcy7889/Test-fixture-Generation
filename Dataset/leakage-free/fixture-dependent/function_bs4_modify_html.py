from bs4 import BeautifulSoup

def modify_html_file(file_path, tag_to_remove=None, new_title=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        if tag_to_remove:
            for tag in soup.find_all(tag_to_remove):
                tag.decompose()

        if new_title:
            title_tag = soup.find('title')
            if title_tag:
                title_tag.string = new_title

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True

    except Exception as e:
        raise Exception(e)