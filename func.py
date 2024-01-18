import math

def dist(vmax, a, d, t1): 
    # v = a * t
    # b = math.sqrt(a^2-vmax^2)
    triangle_base = vmax/a
    rectangle_base = d/vmax -vmax/a
    if t1 <= triangle_base: 
        return t1*a*t1/2
    if t1 > triangle_base and t1 < triangle_base+rectangle_base:
        return triangle_base*vmax + vmax*(t1-triangle_base)
    if t1 >= triangle_base + rectangle_base and t1 <= triangle_base*2+rectangle_base:
        return (triangle_base*vmax)/2+(rectangle_base)*vmax + d-(triangle_base*2+rectangle_base-t1)*a*t1/2
    return d
        



    

