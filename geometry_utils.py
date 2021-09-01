from shapely.geometry import Polygon

def calculate_polygon_iou(points1,points2):
    poly1 = Polygon(points1)
    poly2 = Polygon(points2)
    # ratio of intersection area to union area
    iou = poly1.intersection(poly2).area/poly1.union(poly2).area
    return iou
    
def points_of_one_detection_result(result):
    p = [(float(result["x1"]), float(result["y1"])),
        (float(result["x2"]), float(result["y2"])),
        (float(result["x3"]), float(result["y3"])),
        (float(result["x4"]), float(result["y4"]))]  
    return p