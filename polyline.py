from ground.base import get_context, Relation
import random
import numpy as np
import matplotlib.pyplot as plt

def polyline_generator(n:int, x_range:tuple=(0,64), y_range:tuple=(0,64), distance_range:tuple=(12,42), angle_range:tuple=(-np.pi/1.5, np.pi/1.5)):
    x_min, x_max = x_range
    y_min, y_max = y_range
    
    if n < 4:
        raise ValueError("n must be at least 4")
    
    context = get_context()
    Point, Contour, Segment = context.point_cls, context.contour_cls, context.segment_cls
    
    # last points
    last_points = [Point(int(x_max - (x_max-x_min)*0.1), int((y_max - y_min)/2)) , Point(x_max, int((y_max - y_min)/2))]
    
    # add first two points manually
    points = [Point(x_min, int((y_max - y_min)/2)), Point(int(x_min + (x_max-x_min)*0.1), int((y_max - y_min)/2))]
    yield [points[0].x, points[0].y]
    yield [points[1].x, points[1].y]
    
    while len(points)<=n-3:
        
        # create point that gets appended to the polyline. Distance to previous point must in the range of
        # distance and angle between the previous to points to this point and the previous point must be in range of angle_range
        angle = random.uniform(*angle_range)
        angle_prev = np.arctan2(points[-1].y-points[-2].y, points[-1].x-points[-2].x)
        distance = random.uniform(*distance_range)
        
        # calculate new point
        x = points[-1].x + distance * np.cos(angle_prev + angle)
        y = points[-1].y + distance * np.sin(angle_prev + angle)
        new_point = Point(int(x), int(y))
        
        # check if new point is within bounds
        if new_point.x < x_min or new_point.x > x_max or new_point.y < y_min or new_point.y > y_max:
            continue
        
        # check if new point intersects with any existing segment
        intersects = False
        for i in range(len(points)-1):
            segment1 = Segment(points[i], points[i+1])
            segment2 = Segment(points[-1], new_point)
            relation = context.segments_relation(segment1, segment2)
            if relation == Relation.CROSS:
                intersects = True
                break
        
        if not intersects:
            points.append(new_point)
            yield [new_point.x, new_point.y]
    
    # add last two points manually
    points.append(last_points[0])
    points.append(last_points[1])
    yield [last_points[0].x, last_points[0].y]
    yield [last_points[1].x, last_points[1].y]
        
if __name__=="__main__":
    for i in polyline_generator(6):
        print(i)