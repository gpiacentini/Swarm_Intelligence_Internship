from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
import numpy as np

from src.simulator import Hook
from src.logger import GlobalLogger

class CoverageMetric(Hook):
    def __init__(self, cfg):
        pass

    def start(self, objects):
        pass
    
    def tick(self, objects):
        pass


    def end(self, object):
        pass