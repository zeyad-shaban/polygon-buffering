import math
import matplotlib.pyplot as plt

# this i already existing in the editor


def findIntersectionUsingPoints(p1, p2, p3, p4):
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
# end


def polygon_signed_area(points: list) -> float:
    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += (x1 * y2 - x2 * y1)
    return area / 2.0


def normalize(vector: list):
    mag = math.sqrt(vector[0]**2 + vector[1]**2)
    return [vector[0] / mag, vector[1] / mag]


def shiftVector(vec, direction, d):
    length = math.sqrt(direction[0]**2 + direction[1]**2)
    direction_unit = [direction[0] / length, direction[1] / length]

    shifted_vec = [vec[0] + d * direction_unit[0],
                   vec[1] + d * direction_unit[1]]

    return shifted_vec


def generateOuterPolyForRunway(points: list, d: float) -> list:
    outerPnts = []
    area = polygon_signed_area(points)
    if area > 0:
        d = -d

    for i, thisPnt in enumerate(points):
        prevPnt = points[i - 1]
        nextPnt = points[(i + 1) % len(points)]

        if i == 0:
            thisNext = [nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1]]
            thisNext_normal_unit = normalize([-thisNext[1], thisNext[0]])
            pointNormal_unit = thisNext_normal_unit
        elif i == len(points) - 1:
            prevThis = [thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1]]
            prevThis_normal_unit = normalize([-prevThis[1], prevThis[0]])
            pointNormal_unit = prevThis_normal_unit
        else:
            prevThis = [thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1]]
            thisNext = [nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1]]
            prevThis_normal_unit = normalize([-prevThis[1], prevThis[0]])
            thisNext_normal_unit = normalize([-thisNext[1], thisNext[0]])

            prevShifted = shiftVector(prevPnt, prevThis_normal_unit, d)
            thisShifted1 = shiftVector(thisPnt, prevThis_normal_unit, d)
            thisShifted2 = shiftVector(thisPnt, thisNext_normal_unit, d)
            nextShifted = shiftVector(nextPnt, thisNext_normal_unit, d)

            intersection = findIntersectionUsingPoints(prevShifted, thisShifted1, thisShifted2, nextShifted)
            outerPnts.append(intersection)

            continue

        pointNormal_scaled = [pointNormal_unit[0] * d, pointNormal_unit[1] * d]
        movedPoint = [thisPnt[0] + pointNormal_scaled[0], thisPnt[1] + pointNormal_scaled[1]]
        outerPnts.append(movedPoint)

    return outerPnts


inX = [
    0, 1, 2, 3
]

inY = [
    0, 2, 1, 3
]


input_ = [[inX[i], inY[i]] for i in range(len(inX))]
outer_out = generateOuterPolyForRunway(input_, 0.5)
inner_out = generateOuterPolyForRunway(input_, -0.5)

outer_X = [pnt[0] for pnt in outer_out]
outer_Y = [pnt[1] for pnt in outer_out]

inner_X = [pnt[0] for pnt in inner_out]
inner_Y = [pnt[1] for pnt in inner_out]

# plotting
fig = plt.figure(dpi=100)

plt.plot(inX, inY)  # how to color, how to make dotted line
plt.plot(outer_X, outer_Y, linestyle="--", color="red")
plt.plot(inner_X, inner_Y, linestyle="--", color="green")

plt.show()
