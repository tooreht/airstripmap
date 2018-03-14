"""Airstrip data structures."""

import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class Airstrip(object):
    """Airstrip storage container."""

    def __init__(self, name, latitude, longitude, **kwargs):
        self.name = name
        self.description = kwargs.get('description', "")
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = kwargs.get('altitude', 0.)
        self.status = kwargs.get('status', 'b')

    def __str__(self):
        return "{} {} {} {}m".format(self.name, self.latitude, self.longitude, self.altitude)

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            self.__class__.__name__,
            self.name,
            self.latitude,
            self.longitude,
            dict(
                description=self.description,
                altitude=self.altitude,
                status=self.status
            )
        )

    def __eq__(self, other):
        return (locale.strxfrm(self.name) == locale.strxfrm(other.name))

    def __ne__(self, other):
        return (locale.strxfrm(self.name) != locale.strxfrm(other.name))

    def __lt__(self, other):
        return (locale.strxfrm(self.name) < locale.strxfrm(other.name))

    def __le__(self, other):
        return (locale.strxfrm(self.name) <= locale.strxfrm(other.name))

    def __gt__(self, other):
        return (locale.strxfrm(self.name) > locale.strxfrm(other.name))

    def __ge__(self, other):
        return (locale.strxfrm(self.name) >= locale.strxfrm(other.name))
