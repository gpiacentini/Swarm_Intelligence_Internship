from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
import numpy as np

from src.simulator import Hook
from src.logger import GlobalLogger

def find_neighbour(nodes):
            
            result = []
            for index, ele in enumerate(nodes):
                if index == 0:
                    result.append((None, nodes[index + 1]))
                elif index == len(nodes) - 1:
                    result.append((nodes[index - 1], None))
                else:
                     result.append((nodes[index - 1], nodes[index + 1]))
                return result

# Whitin the class i pass objects, so i have information about all the characteristic of the nodes #

class CoverageMetric(Hook):
    def __init__(self, cfg):
        pass

    def start(self, objects):

        pass
    
    def tick(self, objects):
        pass


    def end(self, object):
        pass