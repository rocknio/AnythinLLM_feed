
class BookInfo:
    _title = ""
    _author = ""
    _content = ""

    def __init__(self, title, author, content):
        self._title = title
        self._author = author
        self._content = content

    def title(self):
        return self._title

    def author(self):
        return self._author

    def content(self):
        return self._content
