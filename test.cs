using System;
using System.Collections.Generic;
using System.Linq;

public class PolygonGenerator
{
    public static double[] Normalize(double[] vector)
    {
        double mag = Math.Sqrt(vector[0] * vector[0] + vector[1] * vector[1]);
        return new double[] { vector[0] / mag, vector[1] / mag };
    }

    public static List<double[]> GenerateOuterPoly(List<double[]> points, double d)
    {
        List<double[]> outerPnts = new List<double[]>();

        for (int i = 0; i < points.Count; i++)
        {
            double[] thisPnt = points[i];
            double[] prevPnt = points[(i - 1 + points.Count) % points.Count];
            double[] nextPnt = points[(i + 1) % points.Count];

            double[] prevThis = { thisPnt[0] - prevPnt[0], thisPnt[1] - prevPnt[1] };
            double[] thisNext = { nextPnt[0] - thisPnt[0], nextPnt[1] - thisPnt[1] };

            double[] prevThis_normal_unit = Normalize(new double[] { -prevThis[1], prevThis[0] });
            double[] thisNext_normal_unit = Normalize(new double[] { -thisNext[1], thisNext[0] });

            double[] pointNormal_unit = Normalize(new double[] { prevThis_normal_unit[0] + thisNext_normal_unit[0], prevThis_normal_unit[1] + thisNext_normal_unit[1] });

            double[] pointNormal_scaled = { pointNormal_unit[0] * d, pointNormal_unit[1] * d };

            double[] movedPoint = { thisPnt[0] + pointNormal_scaled[0], thisPnt[1] + pointNormal_scaled[1] };
            outerPnts.Add(movedPoint);
        }

        return outerPnts;
    }
}
