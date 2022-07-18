import numpy as np

MISS_THRESHOLD=0.5
BAD_MISS_THRESHOLD=1.0

class Line():
    def __init__(self, a, b) -> None:
        self.a = np.array(a)
        self.b = np.array(b)
        self.v = self.b - self.a
        self.l = np.linalg.norm(self.v)
        self.u = self.v / self.l
    
    def get_length(self):
        return self.l

    def get_point(self, t):
        return self.a + t * self.l * self.u

    def get_closest_point(self, p):
        v = p - self.a
        d = np.dot(v, self.u)
        d = max(0, min(d, self.l))
        return self.a + d * self.u

class Circle():
    def __init__(self, c, r) -> None:
        self.c = np.array(c)
        self.r = r

    def get_length(self):
        return 2 * np.pi * self.r

    def get_point(self, t):
        angle = t * 2 * np.pi
        x = np.cos(angle) * self.r
        y = np.sin(angle) * self.r
        return self.c + np.array([x, y])

    def get_closest_point(self, p):
        v = p - self.c
        u = v / np.linalg.norm(v)
        return self.c + self.r * u

class Arc():
    def __init__(self, c, r, s, e) -> None:
        self.c = np.array(c)
        self.r = r
        self.s = np.array(s)
        self.e = np.array(e)
        self.a = self.get_angle(self.e)

    def get_angle(self, p):
        v = p - self.c
        u = self.s - self.c
        angle = np.arctan2(v[1], v[0]) - np.arctan2(u[1], u[0])
        if angle < 0: angle += 2 * np.pi
        return angle
        
    def get_length(self):
        return self.a * self.r

    def get_point(self, t):
        angle = t * self.a
        v = self.s - self.c
        x = np.cos(angle) * v[0] - np.sin(angle) * v[1]
        y = np.sin(angle) * v[0] + np.cos(angle) * v[1]
        return self.c + np.array([x, y])
    
    def get_closest_point(self, p):
        angle = self.get_angle(p)
        angle = max(0, min(angle, self.a))
        return self.get_point(angle / self.a)

def make_polygon(frame_size, circle):

    h, w = frame_size

    if circle == None:
        polygon = [
            Line((0,0), (w,0)),
            Line((w,0), (w,h)),
            Line((w,h), (0,h)),
            Line((0,h), (0,0)),
        ]
        return polygon

    x, y, r = circle

    intersections = []
    is_line = []

    # Upper edge
    if y-r < 0:
        d = np.sqrt(r**2 - (y - 0)**2)
        if x-d > 0: intersections.append((x-d, 0)); is_line.append(True)
        if x+d < w: intersections.append((x+d, 0)); is_line.append(False)

    if len(is_line) == 0 or is_line[-1]:
        intersections.append((w, 0)); is_line.append(True)
    
    # Right edge
    if x+r > w:
        d = np.sqrt(r**2 - (x - w)**2)
        if y-d > 0: intersections.append((w, y-d)); is_line.append(True)
        if y+d < h: intersections.append((w, y+d)); is_line.append(False)
    
    if is_line[-1]:
        intersections.append((w, h)); is_line.append(True)

    # Bottom edge
    if y+r > h:
        d = np.sqrt(r**2 - (y - h)**2)
        if x+d < w: intersections.append((x+d, h)); is_line.append(True)
        if x-d > 0: intersections.append((x-d, h)); is_line.append(False)

    if is_line[-1]:
        intersections.append((0, h)); is_line.append(True)

    # Left edge
    if x-r < 0:
        d = np.sqrt(r**2 - (x - 0)**2)
        if y+d < h: intersections.append((0, y+d)); is_line.append(True)
        if y-d > 0: intersections.append((0, y-d)); is_line.append(False)

    if is_line[-1]:
        intersections.append((0, 0)); is_line.append(True)

    if len(intersections) == 0:
        polygon = [
            Circle((x, y), r)
        ]
        return polygon

    start = intersections
    end = intersections[1:] + intersections[:1]

    polygon = []
    for s, e, line in zip(start, end, is_line):
        if line:
            segment = Line(s, e)
        else:
            segment = Arc((x, y), r, s, e)
        polygon.append(segment)

    return polygon

def get_polygon_points(polygon, n_points):

    lengths = [seg.get_length() for seg in polygon]
    total_length = sum(lengths)

    step = total_length / n_points
    
    points = []

    for seg, length in zip(polygon, lengths):

        # No need to discretise lines, finaly point pair 
        # will never be in the middle of the line
        if isinstance(seg, Line):
            points.append(seg.b)
            continue

        seg_number = length // step
        for i in range(int(seg_number), 0, -1):
            point = seg.get_point(i / seg_number)
            points.append(point)

    return points

def get_smallest_dist(polygon, point):
    smallest_dist = 1e9
    other_point = None
    for seg in polygon:
        closest = seg.get_closest_point(point)
        dist = np.linalg.norm(point - closest)
        if dist < smallest_dist:
            smallest_dist = dist
            other_point = closest
    return smallest_dist, other_point

def content_area_hausdorff(circle_a, circle_b, frame_size, n_points=100, normalise=True):

    if (circle_a == circle_b):
        return 0.0, None

    polygon_a = make_polygon(frame_size, circle_a)
    polygon_b = make_polygon(frame_size, circle_b)

    points_a = get_polygon_points(polygon_a, n_points)
    points_b = get_polygon_points(polygon_b, n_points)

    hausdorff_distance = 0.0
    best_pair = None

    for point in points_b:
        dist, other_point = get_smallest_dist(polygon_a, point)
        if dist > hausdorff_distance:
            hausdorff_distance = dist
            best_pair = (point, other_point)

    for point in points_a:
        dist, other_point = get_smallest_dist(polygon_b, point)
        if dist > hausdorff_distance:
            hausdorff_distance = dist
            best_pair = (point, other_point)

    if normalise:
        hausdorff_distance = hausdorff_distance * np.linalg.norm([1080, 1920]) / np.linalg.norm(frame_size)

    return hausdorff_distance, best_pair
