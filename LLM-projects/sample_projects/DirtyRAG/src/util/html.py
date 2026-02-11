import re


def clean_html(html_string: str) -> str:
    # Remove all class attributes
    html_string = re.sub(r'\bclass="[^"]*"', "", html_string)

    # Remove attributes that start with "js"
    html_string = re.sub(r'\b(js\w+)="[^"]*"', "", html_string)

    # Remove attributes that start with "svg"
    html_string = re.sub(r'\b(svg\w+)="[^"]*"', "", html_string)

    # Remove links (href attributes)
    html_string = re.sub(r'\bhref="[^"]*"', "", html_string)

    # Remove aria attributes
    html_string = re.sub(r'\baria-\w+="[^"]*"', "", html_string)

    # Remove style attributes
    html_string = re.sub(r'\bstyle="[^"]*"', "", html_string)

    # Remove SVG elements completely
    html_string = re.sub(r"<svg[^>]*>.*?</svg>", "", html_string, flags=re.DOTALL)

    # Remove empty attributes
    html_string = re.sub(r'\s+\w+=""', "", html_string)

    # Remove extra spaces
    html_string = re.sub(r"\s+", " ", html_string)

    # No parens
    html_string = remove_parens(html_string)

    return html_string.strip()


def remove_parens(text: str) -> str:
    return text.replace("(", "").replace(")", "")
