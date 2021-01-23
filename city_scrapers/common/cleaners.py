from unicodedata import normalize
from w3lib.html import remove_tags

UNICODE_FORM = "NFKD"

"""
Remove HTML tags, normalize to Unicode, and strip left and right whitespace. 
"""


def scrub_html(token: str) -> str:
    assert type(token) is str
    token = remove_tags(token)
    token = normalize(UNICODE_FORM, token)
    token = token.strip()
    return token
