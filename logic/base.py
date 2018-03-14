"""Logic base classes"""

class Logic(object):
    """Base logic class, defines contracts for inheriting classes.
    
    +------+     +-----+     +-------+
    | READ | --> | MAP | --> | WRITE |
    +------+     +-----+     +-------+

    The csv2kml programm operates in 3 stages:
    1. Read input files and prepare them for stage 2
    2. Map values from input files to internal data structure and apply business logic
    3. Write generated internal data structure from stage 2 to output
    """
    def __init__(self, in_paths, out_path):
        self.in_paths = in_paths
        self.out_path = out_path

    def read(self):
        raise NotImplementedError

    def map(self, raw):
        raise NotImplementedError

    def write(self, airstrips):
        raise NotImplementedError

    def run(self):
        return self.write(self.map(self.read()))
