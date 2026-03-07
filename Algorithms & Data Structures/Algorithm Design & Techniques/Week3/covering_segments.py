# Uses python3
import sys
from collections import namedtuple

# Task. Given a set of n segments {[a[0], b[0]], [a[1], b[1]], . . . , [a[n−1], b[n−1]]} with integer coordinates on a line, find
# the minimum number m of points such that each segment contains at least one point. That is, find a
# set of integers X of the minimum size such that for any segment [a[i], b[i]] there is a point x ∈ X such
# that a[i] <= x <= b[i].
# Input Format. The first line of the input contains the number n of segments. Each of the following 𝑛 lines
# contains two integers a[i] and b[i] (separated by a space) defining the coordinates of endpoints of the i-th
# segment.
# Output Format. Output the minimum number m of points on the first line and the integer coordinates
# of m points (separated by spaces) on the second line. You can output the points in any order. If there
# are many such sets of points, you can output any set. (It is not difficult to see that there always exist
# a set of points of the minimum size such that all the coordinates of the points are integers.)

# Greedy algorithm: Take the ending coordinate of the leftmost segment and process the segments in an ascending order until it's no longer cover the coordinate.
# For every pair of segments, either s[i] and s[j] overlap each other or not.
# Case 1: s[i] and s[j] does not overlap each other. The optimal solution have two points. The greedy algorithm is consistent with ths optimal solution as
# we pick ending coordinates of s[i] and s[j] as solutions.
# Case 2: s[i] and s[j] overlaps. There must exist a point that both segments cover. The greey algorithm is consistent with this optimal solution as
# the left-most segment, say s[i] (if s[i].end < s[j].end), must have some area covered by s[j]. The worst case is the ending coordinate.
# So, picking the left segment is a safe move.

Segment = namedtuple("Segment", "start end")


def min_segments(
    segments,
):  # return the index of the left-most segment by a linear search on the 'end' coordinate of segment
    index = 0
    for i in range(len(segments)):
        if segments[i].end < segments[index].end and index != i:
            index = i
    return index


def optimal_points(segments):
    points = []  # A set of points to be covered by segments
    segments_copy = segments.copy()
    anchor = 0  # Current point for processing which will be reinitialized in the loop
    for i in range(len(segments)):
        argmin_index = min_segments(segments_copy)
        s = segments_copy[argmin_index]  # Extract the left-most segment
        if (
            i == 0
        ):  # If it is the first left-most segment, the ending coordinate must be a solution
            anchor = s.end
            points.append(anchor)
        else:  # for the remaining left-most segment, if the segment does not cover the previous fix point, then we need to construct a new point using ending coordinate
            if not ((s.start <= anchor) and (anchor <= s.end)):
                anchor = s.end
                points.append(anchor)
        del segments_copy[
            argmin_index
        ]  # Delete the left-most segment for the next search
    return points


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    print(*points)
