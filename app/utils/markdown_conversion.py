# utils.py
import markdown2


def convert_markdown_to_html(markdown_text):
    return markdown2.markdown(markdown_text)
