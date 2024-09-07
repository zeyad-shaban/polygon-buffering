import numpy as np

def find_intersection(vec1=None, vec2=None, p1=None, p2=None, p3=None, p4=None):
    if vec1 is not None and vec2 is not None:
        # Convert vectors to points
        p1 = [0, 0]
        p2 = vec1
        p3 = [0, 0]
        p4 = vec2

    # Line 1 represented as a1x + b1y = c1
    a1 = p2[1] - p1[1]
    b1 = p1[0] - p2[0]
    c1 = a1 * p1[0] + b1 * p1[1]

    # Line 2 represented as a2x + b2y = c2
    a2 = p4[1] - p3[1]
    b2 = p3[0] - p4[0]
    c2 = a2 * p3[0] + b2 * p3[1]

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None  # Lines are parallel and do not intersect

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    return [x, y]

# Example usage:
vec1 = [1, 0]
vec2 = [0, -1]
print(find_intersection(vec1=vec1, vec2=vec2))  # Output: [0.0, 0.0]

p1 = [1, 1]
p2 = [2, 1]
p3 = [4, 4]
p4 = [4, 3]
print(find_intersection(p1=p1, p2=p2, p3=p3, p4=p4))  # Output: [4.0, 1.0]
