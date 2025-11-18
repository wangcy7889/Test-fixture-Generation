from bs4 import BeautifulSoup

class HTMLTableFile:
    def __init__(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError("Error: file_path It must be of string type")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.html = f.read()
        except Exception as e:
            raise ValueError(f"Error: Unable to read the file: {e}")

def extract_table_from_html(html_table_file):
    if not isinstance(html_table_file, HTMLTableFile):
        raise TypeError("Error: The parameter must be HTMLTableFile Type instance")
    soup = BeautifulSoup(html_table_file.html, "html.parser")
    table = soup.find("table")
    if not table:
        return []
    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        rows.append([cell.get_text(strip=True) for cell in cells])
    return rows

