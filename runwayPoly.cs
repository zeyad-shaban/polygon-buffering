public static List<Coordinates> GenerateOuterPolyForRunway(List<Coordinates> points_cords, double d)
{
    List<double[]> outerPnts = new List<double[]>();

    // Convert points to double[] and from lat, long to X, Y
    List<double[]> points = new List<double[]>();
    foreach (Coordinates pnt in points_cords)
    {
        points.Add(convertLatLonToXY(pnt.X, pnt.Y));
    }

    // Calculate signed area
    double area = PolygonSignedArea(points);
    d = Math.Abs(d);
    if (area > 0) d = -d;

    // Generate outer polygon points
    for (int i = 0; i < points.Count; i++)
    {
        double[] thisPnt = points[i];
        double[] prevPnt = points[(i - 1 + points.Count) % points.Count];
        double[] nextPnt = points[(i + 1) % points.Count];

        if (i == 0) // Special case for the first point
        {
            double[] thisNext = { nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1] };
            double[] thisNext_normal_unit = Normalize(new double[] { -thisNext[1], thisNext[0] });
            double[] pointNormal_unit = thisNext_normal_unit;

            double[] pointNormal_scaled = { pointNormal_unit[0] * d, pointNormal_unit[1] * d };
            double[] movedPoint = { thisPnt[0] + pointNormal_scaled[0], thisPnt[1] + pointNormal_scaled[1] };
            outerPnts.Add(movedPoint);
        }
        else if (i == points.Count - 1) // Special case for the last point
        {
            double[] prevThis = { thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1] };
            double[] prevThis_normal_unit = Normalize(new double[] { -prevThis[1], prevThis[0] });
            double[] pointNormal_unit = prevThis_normal_unit;

            double[] pointNormal_scaled = { pointNormal_unit[0] * d, pointNormal_unit[1] * d };
            double[] movedPoint = { thisPnt[0] + pointNormal_scaled[0], thisPnt[1] + pointNormal_scaled[1] };
            outerPnts.Add(movedPoint);
        }
        else // General case for the middle points
        {
            double[] prevThis = { thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1] };
            double[] thisNext = { nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1] };

            double[] prevThis_normal_unit = Normalize(new double[] { -prevThis[1], prevThis[0] });
            double[] thisNext_normal_unit = Normalize(new double[] { -thisNext[1], thisNext[0] });

            // Shift vectors
            double[] prevShifted = ShiftVector(prevPnt, prevThis_normal_unit, d);
            double[] thisShifted1 = ShiftVector(thisPnt, prevThis_normal_unit, d);
            double[] thisShifted2 = ShiftVector(thisPnt, thisNext_normal_unit, d);
            double[] nextShifted = ShiftVector(nextPnt, thisNext_normal_unit, d);

            // Find intersection
            double[] intersection = FindIntersectionUsingPoints(prevShifted, thisShifted1, thisShifted2, nextShifted);
            outerPnts.Add(intersection);
        }
    }

    // Convert points to coordinates, and from x, y to lat, long
    List<Coordinates> outerPnts_cords = new List<Coordinates>();
    foreach (double[] pnt in outerPnts)
    {
        double[] pointLatLon = convertXYToLatLon(pnt[0], pnt[1]);
        outerPnts_cords.Add(new Coordinates(pointLatLon[1], pointLatLon[0]));
    }

    return outerPnts_cords;
}

// Helper function to normalize a vector
public static double[] Normalize(double[] vec)
{
    double length = Math.Sqrt(vec[0] * vec[0] + vec[1] * vec[1]);
    return new double[] { vec[0] / length, vec[1] / length };
}

// Helper function to shift a vector
public static double[] ShiftVector(double[] vec, double[] direction, double d)
{
    double length = Math.Sqrt(direction[0] * direction[0] + direction[1] * direction[1]);
    double[] direction_unit = { direction[0] / length, direction[1] / length };

    return new double[]
    {
        vec[0] + d * direction_unit[0],
        vec[1] + d * direction_unit[1]
    };
}

// Helper function to find intersection
public static double[] FindIntersectionUsingPoints(double[] p1, double[] p2, double[] p3, double[] p4)
{
    double a1 = p2[1] - p1[1];
    double b1 = p1[0] - p2[0];
    double c1 = a1 * p1[0] + b1 * p1[1];

    double a2 = p4[1] - p3[1];
    double b2 = p3[0] - p4[0];
    double c2 = a2 * p3[0] + b2 * p3[1];

    double determinant = a1 * b2 - a2 * b1;

    if (determinant == 0)
    {
        return null; // Lines are parallel and do not intersect
    }

    double x = (b2 * c1 - b1 * c2) / determinant;
    double y = (a1 * c2 - a2 * c1) / determinant;

    return new double[] { x, y };
}