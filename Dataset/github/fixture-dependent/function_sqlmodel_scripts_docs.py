import re
from pathlib import Path
import mkdocs.utils
import typer
from jinja2 import Template
en_docs_path = Path('')
index_sponsors_template = '\n{% if sponsors %}\n{% for sponsor in sponsors.gold -%}\n<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>\n{% endfor -%}\n{%- for sponsor in sponsors.silver -%}\n<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>\n{% endfor %}\n{% endif %}\n'
app = typer.Typer()

def generate_readme_content() -> str:
    en_index = en_docs_path / 'docs' / 'index.md'
    content = en_index.read_text('utf-8')
    match_pre = re.search('</style>\\n\\n', content)
    match_start = re.search('<!-- sponsors -->', content)
    match_end = re.search('<!-- /sponsors -->', content)
    sponsors_data_path = en_docs_path / 'data' / 'sponsors.yml'
    sponsors = mkdocs.utils.yaml_load(sponsors_data_path.read_text(encoding='utf-8'))
    if not (match_start and match_end):
        raise RuntimeError("Couldn't auto-generate sponsors section")
    if not match_pre:
        raise RuntimeError("Couldn't find pre section (<style>) in index.md")
    frontmatter_end = match_pre.end()
    pre_end = match_start.end()
    post_start = match_end.start()
    template = Template(index_sponsors_template)
    message = template.render(sponsors=sponsors)
    pre_content = content[frontmatter_end:pre_end]
    post_content = content[post_start:]
    new_content = pre_content + message + post_content
    new_content = re.sub('<!-- only-mkdocs -->.*?<!-- /only-mkdocs -->', '', new_content, flags=re.DOTALL)
    return new_content