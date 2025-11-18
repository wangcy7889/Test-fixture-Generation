from mistune import create_markdown


def convert_to_html(markdown_text: str, html_level: int = None) -> str:
    if html_level is None:
        raise ValueError("Error: html_level is required (1, 2, or 3)")

    if not isinstance(html_level, int) or html_level not in [1, 2, 3]:
        raise ValueError("Error: html_level must be 1 (basic), 2 (intermediate), or 3 (advanced)")

    plugins = []
    if html_level >= 1:
        plugins.append('strikethrough')
    if html_level >= 2:
        plugins.append('footnotes')
    if html_level >= 3:
        plugins.append('table')

    markdown = create_markdown(plugins=plugins)

    if not isinstance(markdown_text, str):
        raise ValueError("Error: Input must be a string")

    if not markdown_text.strip():
        raise ValueError("Error: Input cannot be empty")

    return markdown(markdown_text)

