#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""Check the 'wikipedia philosophy law'."""


from contextlib import closing
from html.parser import HTMLParser
import time
from urllib.parse import quote, unquote
from urllib.request import urlopen

import lxml.html


BASE_PATH = u'http://ru.wikipedia.org'


class LinkSearchError(Exception):
    pass


def is_link_valid(attributes):
    href = attributes['href']
    if not href.startswith('/wiki/'):
        return False

    try:
        img_class = attributes[u'class']
    except KeyError:
        return True

    if img_class in [u'image']:
        return False

    return True


class MainTextLinksGetter(HTMLParser):

    """Class for extracting main article text from wikipedia articles."""

    GARBAGE_CLASSES = set([
        "infobox",
        "noprint",
        "image",
        "internal",
        "toc",
        "reference",
        "dablink",
        "thumbinner",
        "navbox",
        'new'

    ])

    GARBAGE_TAGS = set([
        "table",
        'i'
    ])

    def __init__(self):
        HTMLParser.__init__(self)
        self.main_text = False
        self.main_text_div_depth = 0
        self.garbage_class_depth = 0
        self.brackets_depth = 0
        self.links = []

    def check_garbage_depth(self, tag, attrs):
        if self.garbage_class_depth > 0:
            self.garbage_class_depth += 1
        else:
            tag_classes = set(attrs.get("class", "").split())

            if (self.GARBAGE_CLASSES.intersection(tag_classes) or
                    tag in self.GARBAGE_TAGS):
                self.garbage_class_depth = 1

        return self.garbage_class_depth

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        self.check_garbage_depth(tag, attrs_dict)

        if tag == 'div':
            if self.main_text:
                self.main_text_div_depth += 1
            else:
                try:
                    if attrs_dict['id'] == 'mw-content-text':
                        assert not self.main_text, \
                            "There can be only one main block."
                        self.main_text = True
                except KeyError:
                    pass
        elif tag == 'a':
            if (self.main_text and
                    self.brackets_depth == 0 and
                    # self.main_text_div_depth == 0 and
                    self.garbage_class_depth == 0):
                try:
                    if is_link_valid(attrs_dict):
                        self.links.append(attrs_dict['href'])
                except KeyError:
                    pass

    def handle_endtag(self, tag):
        if self.garbage_class_depth > 0:
            self.garbage_class_depth -= 1

        if tag == 'div':
            if self.main_text_div_depth == 0:
                self.main_text = False
            else:
                self.main_text_div_depth -= 1

    def handle_data(self, data):
        if self.main_text:
            for symbol in data:
                if symbol == u'(':
                    self.brackets_depth += 1
                elif symbol == u')':
                    self.brackets_depth -= 1


def find_first_link(html):
    parser = MainTextLinksGetter()
    parser.feed(html)

    if not parser.links:
        raise LinkSearchError("Valid links not found")

    return str(parser.links[0])


def philosophy_chain(base_name, max_iters=100):
    visited = set([base_name])
    next_name = base_name
    print(unquote(str(base_name)))
    for _ in range(max_iters):
        time.sleep(0.2)
        url = BASE_PATH + next_name
        with closing(urlopen(url)) as conn:
            html = conn.read().decode('utf-8')

        try:
            next_name = find_first_link(html)
        except LinkSearchError:
            break

        name = unquote(str(next_name))
        print(name)
        if name in visited:
            return False
        visited.add(name)
        if name == u'/wiki/Философия':
            return True
    return False


def main():
    link = u'/wiki/'+input('Введите название статьи с заглавной буквы')
    start = quote(link.encode('utf-8'))
    res = philosophy_chain(start)
    print("Philosophy found:", res)


if __name__ == '__main__':
    main()
