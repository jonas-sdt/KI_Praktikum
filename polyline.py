from bentley_ottmann.planar import contour_self_intersects
from ground.base import get_context
import random
import numpy as np
import matplotlib.pyplot as plt

def polyline(num_points:int = 6):
    
    intersects = True
    contour = None
    while intersects:
        context = get_context()
        Point, Segment = context.point_cls, context.segment_cls
        Contour = context.contour_cls
        # generate random points
        points = [Point(0,32)]
        for i in range(num_points):
            solvable = False
            x = 32
            y = 0
            i = 0
            while(not solvable):
                angle = random.uniform(0, 2 * np.pi)
                distance = random.uniform(4, 24)
                x = points[i-1].x + int(distance * np.cos(angle))
                y = points[i-1].y + int(distance * np.sin(angle))

                if x < 0 or x > 64 or y < 0 or y > 64:
                    continue
                if i>1:
                    # distance between last two points
                    if np.sqrt((x - points[i-2][0])**2 + (y - points[i-2][0])**2) < 4:
                        continue
                    
                    # angle not too sharp
                    if np.arctan2(points[i-2][1] - y, points[i-2][0] - x) - np.arctan2(points[i-1][1] - y, points[i-1][0] - x) < np.pi/2:
                        continue
                    else:
                        solvable = True
                        i+=1
                else:
                    solvable = True
                    i += 1
            points.append(Point(x, y))

        points.append(Point(64, 32))

        # create the polyline

        contour = Contour(points)
        
        intersects = contour_self_intersects(contour)


    contour = np.array(contour.vertices)
    x = [i.x for i in contour]
    y = [i.y for i in contour]
    
    return np.array([x,y]).T
    