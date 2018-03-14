""""CSV parsing."""


import pandas

from pathlib import PurePath
from .base import Reader


class HajaReader(Reader):
    KEYS = ["Name", "ICAO", "Latitude", "Longitude", "Open", "Usage"]

    def read(self, pure_path):
        data = None
        if pure_path.suffix == ".csv":
            # Parse csv into a pandas DataFrame
            df = pandas.read_csv(pure_path)
            # Skip empty rows
            df.dropna(how="all", inplace=True)
            # Drop duplicate ICAO entries for indexing
            df.drop_duplicates(subset=["ICAO"], keep='first', inplace=True)
            # Check csv file type
            if sorted(df.keys()) == sorted(self.KEYS):
                data = df.set_index("ICAO")  # Set index on airstrip ICAO
        return "haja", data


class WingmanReader(Reader):
    KEYS = ["Abbreviation", "Name", "ICAO", "Latitude", "Longitude", "Elev (ft)",
       "Ctry", "Owner", "Avgas", "Jet", "Direction", "Class", "Surface",
       "Length", "Width", "Comments", "Last Insp", "Freq (mths)", "Closed",
       "Waypt. Only", "Dep. Tax"]

    def read(self, pure_path):
        data = None
        if pure_path.suffix == ".csv":
            # Parse csv into a pandas DataFrame
            df = pandas.read_csv(pure_path)
            # Skip empty rows
            df.dropna(how="all", inplace=True)
            # Drop duplicate ICAO entries for indexing
            df.drop_duplicates(subset=["ICAO"], keep='first', inplace=True)
            # Check csv file type
            if sorted(df.keys()) == sorted(self.KEYS):
                data = df.set_index("ICAO")  # Set index on airstrip ICAO
        return "wingman", data
