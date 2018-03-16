"""Haja-Wingman logic implementation."""

import logging
import math
import numpy as np

import conversions
import readers
import writers

from collections import defaultdict
from pathlib import PurePath
from .airstrip import Airstrip
from .base import Logic


logger = logging.getLogger('cli')


def build_description(icao, h, w):
    meta = defaultdict(str, {
        "icao": icao,
        "closed": "-",
        "class": "-",
        "usage": "-",
        "surface": "-",
        "length": "-",
        "width": "-",
        "inspection": "-",
        "owner": "-",
        "comments": "-",
    })
    if h is not None:
        meta.update({
            "closed": "Yes" if h.Open == "Closed" else "No",
            "usage": h.Usage,
        })
    if w is not None:
        meta.update({
            "class": w.Class if isinstance(w.Class, str) else "-",
            "surface": w.Surface if isinstance(w.Surface, str) else "-",
            "length": w.Length if isinstance(w.Length, str) else "-",
            "width": w.Width if isinstance(w.Width, str) else "-",
            "inspection": w["Last Insp"] if isinstance(w["Last Insp"], str) else "-",
            "owner": w.Owner if isinstance(w.Owner, str) else "-",
            "comments": w.Comments if isinstance(w.Comments, str) else "-",
        })
        if not meta.get("closed") == "Yes":
            meta.update(closed=w.Closed)
    return (
        "ICAO: {icao}, "
        "Closed: {closed}, "
        "Class: {class}, "
        "Usage: {usage}, "
        "Surface: {surface}, "
        "Length: {length}, "
        "Width: {width}, "
        "last Inspection: {inspection}, "
        "Owner: {owner}, "
        "Comments: {comments}".format(**meta)
    )

def build_altitude(altitude):
    if isinstance(altitude, str):
        altitude = altitude.strip('ft')
    try:
        altitude = float(altitude)
    except ValueError:
        altitude = 0.

    if math.isnan(altitude):
        altitude = 0.

    return altitude


class HajaWingmanLogic(Logic):
    """Logic implementing kml generation out of the haja and wingman csv files.

                                            Logic
    haja.csv ------+                   +-----------------+
                   |     +------+      | validate   skip |      +-------+
                   +---> | READ | ---> |       MAP       | ---> | WRITE | --> airstrips.kml
                   |     +------+      | convert   merge |      +-------+
    wingman.csv ---+                   +-----------------+
    """
    readers = [readers.csv.HajaReader, readers.csv.WingmanReader]

    def read(self):
        total_files = len(self.in_paths)
        read_files = 0
        raw = {}
        while len(self.in_paths) > 0:
            pp = PurePath(self.in_paths.pop())
            for reader in self.readers:
                name, data = reader().read(pp)
                if data is not None:
                    raw[name] = data
                    read_files += 1
        # Logging
        out = "{} of {} file(s) read.".format(read_files, total_files)
        logger.info(out)
        print(out)

        return raw

    def map(self, raw):
        haja_df = raw['haja']
        wingman_df = raw['wingman']

        # Create a unique list of ICAOs
        icaos = set(haja_df.index.tolist()) | set(wingman_df.index.tolist())
        icaos.remove(np.nan)

        airstrips = []
        for icao in icaos:
            h, w = None, None
            if icao in haja_df.index:
                h = haja_df.loc[icao]
            if icao in wingman_df.index:
                w = wingman_df.loc[icao]
                if w.Ctry != "MG":  # Skip airstrips outside Madagascar
                    logger.warning("{} is outside Madagascar, skipping...".format(icao))
                    continue

            if not (h is None or w is None):
                name = h.Name
                description = build_description(icao, h, w)
                latitude = w.Latitude
                longitude = w.Longitude
                altitude = build_altitude(w['Elev (ft)'])
                if h.Open == "Closed" or w.Closed == "Yes":
                    status = "x"
                elif w.Class in ["A", "B", "C"]:
                    status = w.Class.lower()
                else:
                    status = "c"  # Conservative assumption
            elif h is not None:
                name = h.Name
                description = build_description(icao, h, None)
                latitude = h.Latitude
                longitude = h.Longitude
                altitude = 0.
                if h.Open == "Closed":
                    status = "x"
                else:
                    status = "c"  # Conservative assumption
            elif w is not None:
                name = w.Name
                description = build_description(icao, None, w)
                latitude = w.Latitude
                longitude = w.Longitude
                altitude = build_altitude(w['Elev (ft)'])
                if w.Closed == "Yes":
                    status = "x"
                elif w.Class in ["A", "B", "C"]:
                    status = w.Class.lower()
                else:
                    status = "c"  # Conservative assumption
            else:
                name = ""
                description = ""
                latitude = ""
                longitude = ""
                altitude = 0.
                status = "c"  # Conservative assumption

            # Skip if required values are invalid
            if (not name or latitude is None or longitude is None
                or latitude is np.nan or longitude is np.nan):
                logger.warning("{} has invalid required values, skipping...".format(icao))
                logger.warning("{} required values: name={}, latitude={}, longitude={}".format(
                    icao, name, latitude, longitude
                ))
                continue

            # Conversions
            words = [word.capitalize() for word in name.split(' ')]
            words = map(lambda x: '/'.join([w.capitalize() for w in x.split('/')]), words)
            name = ' '.join(words)
            latitude = conversions.parse_coord(latitude.strip())
            longitude = conversions.parse_coord(longitude.strip())
            altitude = conversions.feet_to_meters(altitude)

            # Skip invalid coordinates
            if latitude is None or longitude is None:
                logger.warning("{} has invalid coordinates: {}, {}, skipping...".format(icao, latitude, longitude))
                continue

            airstrips.append(
                Airstrip(
                    name=name,
                    description=description,
                    latitude=latitude,
                    longitude=longitude,
                    altitude=altitude,
                    status=status,
                )
            )

        # Retun a airstrip instance list sorted by name
        return sorted(airstrips)

    def write(self, airstrips):
        return writers.kml.write(airstrips, self.out_path)
