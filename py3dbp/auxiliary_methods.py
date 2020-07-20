from decimal import Decimal
from .constants import Axis


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT)
    )

def intersect_area(item1, item2):
    shared_area_proportion = 0.0
    if intersect(item1, item2):
        if(item1.position[0]+item1.dimension[0]<=item2.position[0]+item2.dimension[0]):
            dx = item1.position[0]+item1.dimension[0]-max(item1.position[0],item2.position[0])
        else:
            dx = item2.position[0]+item2.dimension[0]-max(item1.position[0],item2.position[0])
            
        if(item1.position[1]+item1.dimension[1]<=item2.position[1]+item2.dimension[1]):
            dy = item1.position[1]+item1.dimension[1]-max(item1.position[1],item2.position[1])
        else:
            dy = item2.position[1]+item2.dimension[1]-max(item1.position[1],item2.position[1])
        
        w = item2.dimension[0]
        h = item2.dimension[1]
        shared_area_proportion = (float(dx)*float(dy))/(float(w)*float(h))
     
    return shared_area_proportion


def get_limit_number_of_decimals(number_of_decimals):
    return Decimal('1.{}'.format('0' * number_of_decimals))


def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)

    return Decimal(value).quantize(number_of_decimals)
