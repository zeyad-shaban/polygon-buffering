import math
import matplotlib.pyplot as plt


def lat_lon_to_xy(latitudes, longitudes):
    R = 6378137  # Earth's radius in meters
    x_coords = [R * math.radians(lon) for lon in longitudes]
    y_coords = [R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) for lat in latitudes]
    return x_coords, y_coords


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


def generateOuterPoly(points: list, d: float) -> list:
    outerPnts = []
    d = abs(d)
    area = polygon_signed_area(points)
    if area > 0:
        d = -d

    for i in range(len(points)):
        thisPnt = points[i]
        prevPnt = points[i - 1]
        nextPnt = points[(i + 1) % len(points)]

        prevThis = [thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1]]
        thisNext = [nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1]]

        prevThis_normal_unit = normalize([-prevThis[1], prevThis[0]])
        thisNext_normal_unit = normalize([-thisNext[1], thisNext[0]])

        pointNormal_unit = normalize([prevThis_normal_unit[0] + thisNext_normal_unit[0], prevThis_normal_unit[1] + thisNext_normal_unit[1]])

        pointNormal_scaled = [pointNormal_unit[0] * d, pointNormal_unit[1] * d]

        movedPoint = [thisPnt[0] + pointNormal_scaled[0], thisPnt[1] + pointNormal_scaled[1]]
        outerPnts.append(movedPoint)

    return outerPnts


inLat = [
    31.0281690017913,
    33.5129242859397,
    31.616617353979,
    31.1002874883973,
    30.02606053743,
    30.012806236812,
    30.121515206942505,
]

inLon = [
    30.9626576454744,
    29.9906157353342,
    34.690093946563,
    34.4145545074681,
    34.7283633131039,
    32.5240478003451,
    31.362647140376634,
]

inX, inY = lat_lon_to_xy(inLat, inLon)

input = [[inX[i], inY[i]] for i in range(len(inLat))]
output = generateOuterPoly(input, 32000)
outX = [pnt[0] for pnt in output]
outY = [pnt[1] for pnt in output]


outLon = [
    30.739257661569781,
    29.804928911237994,
    34.914414912862185,
    34.651119283299522,
    34.922577683965386,
    32.514998284467879,
    31.225798737824832,
]

outLat = [
    30.902124844491841,
    33.707149167368435,
    31.71133031527577,
    31.066534145981795,
    29.859845174673161,
    29.723865821772616,
    29.880778237839621,
]

outX, outY = lat_lon_to_xy(outLat, outLon)


# plotting
fig = plt.figure(dpi=100)

plt.plot(inX, inY)  # how to color, how to make dotted line
plt.plot(outX, outY, linestyle="--", color="red")

plt.show()
