"""GPS coordinate format conversions.

Reference: https://support.google.com/maps/answer/18539
"""

import logging
import re


logger = logging.getLogger('cli')

# 41°24'12.2"N 2°10'26.5"E
dms_coord = re.compile(r"""^[\d]{1,2}°[\d]{1,2}'[\d]{1,2}(\.[\d]+)?"[NESW]$""")
dms_coords = re.compile(r"""^[\d]{1,2}°[\d]{1,2}'[\d]{1,2}(\.[\d]+)?"[NESW] [\d]{1,2}°[\d]{1,2}'[\d]{1,2}(\.[\d]+)?"[NESW]$""")
# 41 24.2028, 2 10.4418
dmm_coord = re.compile(r"^[\d]{1,2} [\d]{1,2}(\.[\d]+)?$")
dmm_coords = re.compile(r"^[\d]{1,2} [\d]{1,2}(\.[\d]+)?, [\d]{1,2} [\d]{1,2}(\.[\d]+)?$")
# 41.40338, 2.17403
dd_coord = re.compile(r"^[\d]{1,2}.[\d]+$")
dd_coords = re.compile(r"^[\d]{1,2}.[\d]+, [\d]{1,2}.[\d]+$")
# N 41 24 12.2 E 2 10 26.5
hyb1_coord = re.compile(r"^[NESW] [\d]{1,3} [\d]{1,2} [\d]{1,2}(\.[\d]+)?$")
hyb1_coords = re.compile(r"^[NESW] [\d]{1,2} [\d]{1,2} [\d]{1,2}(\.[\d]+)?, [NESW] [\d]{1,3} [\d]{1,2} [\d]{1,2}(\.[\d]+)?$")
# S 41 24.2028 W 2 10.4418
hyb2_coord = re.compile(r"^[NESW] [\d]{1,3} [\d]{1,2}(\.[\d]+)?$")
hyb2_coords = re.compile(r"^[NESW] [\d]{1,2} [\d]{1,2}(\.[\d]+)?, [NESW] [\d]{1,2} [\d]{1,3}(\.[\d]+)?$")


def dms2dd(degrees: str, minutes: str, seconds: str, direction: str) -> float:
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

def dmm2dd(degrees: str, decimal_minutes: str) -> float:
    d = int(degrees)
    dm = float(decimal_minutes)/60
    dd = d + dm
    return dd

def dd2dms(deg: float) -> [int, int, int]:
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def hyb22dd(degrees: str, decimal_minutes: str, direction: str) -> float:
    d = int(degrees)
    dm = float(decimal_minutes)/60
    dd = d + dm
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

def parse_dms_part(dms: str) -> float:
    parts = re.split('[^\d\w]+', dms)
    coord = dms2dd(parts[0], parts[1], parts[2], parts[3])
    return coord

def parse_dmm_part(dmm: str) -> float:
    parts = dmm.split(' ')
    coord = dmm2dd(parts[0], parts[1])
    return coord

def parse_dd_part(dd: str) -> float:
    return float(dd)

def parse_hyb1_part(hyb1: str) -> float:
    parts = hyb1.split(' ')
    coord = dms2dd(parts[1], parts[2], parts[3], parts[0])
    return coord

def parse_hyb2_part(hyb2: str) -> float:
    parts = hyb2.split(' ')
    coord = hyb22dd(parts[1], parts[2], parts[0])
    return coord

def parse_dms(dms: str) -> (float, float):
    """Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E."""
    parts = dms.split(' ')
    lat = parse_dms_part(parts[0])
    lng = parse_dms_part(parts[1])

    return lat, lng

def parse_dmm(dmm:  str) -> (float, float):
    """Degrees and decimal minutes (DMM): 41 24.2028, 2 10.4418."""
    parts = dmm.split(', ')
    lat = parse_dmm_part(parts[0])
    lng = parse_dmm_part(parts[1])

    return lat, lng

def parse_dd(dd: str) -> (float, float):
    """Decimal degrees (DD): 41.40338, 2.17403."""
    parts = dms.split(', ')
    lat = parse_dd_part(parts[0])
    lng = parse_dd_part(parts[1])

    return lat, lng

def parse_hyb1(dmm:  str) -> (float, float):
    """Strange hybrid #1: N 41 24 12.2, E 2 10 26.5."""
    parts = dmm.split(', ')
    lat = parse_hyb1_part(parts[0])
    lng = parse_hyb1_part(parts[1])

    return lat, lng

def parse_hyb2(dmm:  str) -> (float, float):
    """Strange hybrid #2: S 41 24.2028, W 2 10 26.5."""
    parts = dmm.split(', ')
    lat = parse_hyb2_part(parts[0])
    lng = parse_hyb2_part(parts[1])

    return lat, lng

def parse_coord(coord):
    if hyb1_coord.match(coord):
        return parse_hyb1_part(coord)
    elif hyb2_coord.match(coord):
        return parse_hyb2_part(coord)
    elif dms_coord.match(coord):
        return parse_dms_part(coord)
    elif dmm_coord.match(coord):
        return parse_dmm_part(coord)
    elif dd_coord.match(coord):
        return parse_dd_part(coord)
    else:
        logger.warning("Invalid coordinate format {}".format(coord))
        return None

def parse_coords(coords):
    if hyb1_coords.match(coords):
        return parse_hyb1(coords)
    elif hyb2_coords.match(coords):
        return parse_hyb2(coords)
    elif dms_coords.match(coords):
        return parse_dms(coords)
    elif dmm_coords.match(coords):
        return parse_dmm(coords)
    elif dd_coords.match(coords):
        return parse_dd(coords)
    else:
        logger.warning("Invalid coordinates format {}".format(coords))
        return None

def feet_to_meters(feet: float) -> float:
    return feet * 0.3048
