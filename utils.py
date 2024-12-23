import math

def distance(x1, x2, y1, y2, distRequire, moveDist):
    return [[x2-x1 if abs(x2-x1) <= (distRequire[0]+moveDist) and abs(x2-x1) > distRequire[0] else 0], math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )]
