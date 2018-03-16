"""KML generation"""

import logging
import simplekml

from constants import GOV_AIRPORTS
from .components import (
    region,
    green, yellow, orange, red,
    small_airport, medium_airport, big_airport
)


logger = logging.getLogger('cli')

AIRSTRIP_STYLE_MAP = {
    "small": small_airport,
    "medium": medium_airport,
    "big": big_airport,

    "a": green,
    "b": yellow,
    "c": orange,
    "x": red,
}


def style(airstrip):
    key = GOV_AIRPORTS.get(airstrip.name) or airstrip.status
    return AIRSTRIP_STYLE_MAP[key]

def write(airstrips, path):
    # Document
    kml = simplekml.Kml(name="MAF Airstrips", open=1)  # the document will be open in the table of contents

    # Region
    kml.document.region = region

    # Placemarks
    for airstrip in airstrips:
        logger.info(airstrip)
        pnt = kml.newpoint()
        pnt.name = airstrip.name
        pnt.description = airstrip.description
        pnt.coords = [(airstrip.longitude, airstrip.latitude, airstrip.altitude)]
        pnt.style =  style(airstrip)

    # Write kml file
    kml.save(path)

    out = "Generated KML file with {} airstrips.".format(len(airstrips))
    logger.info(out)
    print(out)
