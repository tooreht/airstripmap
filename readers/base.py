"""Reader base classes"""


class Reader(object):
    """Base reader class, defines contracts for inheriting classes."""

    def read(self, path):
        raise NotImplementedError
