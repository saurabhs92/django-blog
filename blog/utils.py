import datetime
import re

from django.utils.html import strip_tags

def count_words():
    html_string = """<h1> This is a title </h1>"""
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count

