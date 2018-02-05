from six import text_type as text
from cgi import parse_header
from normality import stringify
from normality.encoding import normalize_encoding


class MIMEType(object):
    __slots__ = ['family', 'subtype', 'params', 'label']

    SEP = text('/')

    def __init__(self, family, subtype, params=None):
        self.family = family
        self.subtype = subtype
        self.label = None
        if self.family is not None and self.subtype is not None:
            self.label = self.SEP.join((self.family, self.subtype))
        self.params = params

    @property
    def charset(self):
        if self.params is None:
            return
        charset = self.params.get('charset')
        return normalize_encoding(charset, default=None)

    @classmethod
    def split(cls, mime_type):
        if mime_type is None or cls.SEP not in mime_type:
            return None, None
        family, subtype = (stringify(p) for p in mime_type.split(cls.SEP, 1))
        if family is None or subtype is None:
            return None, None
        return family.lower(), subtype.lower()

    @classmethod
    def parse(cls, mime_type, default=None):
        mime_type = stringify(mime_type)
        params = None
        if mime_type is not None:
            mime_type, params = parse_header(mime_type)

        family, subtype = cls.split(mime_type)
        if family is None:
            family, subtype = cls.split(default)
        return cls(family, subtype, params=params)

    def __str__(self):
        return text(self.label or 'application/octet-stream')

    def __repr__(self):
        return self.label
