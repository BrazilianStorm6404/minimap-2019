import cv2
import math
import copy
import time
from networktables import NetworkTables


real_height = 823
real_width = 1646
pixels_height = 495
pixels_width = 1223
class utils:
    def height_px_to_cm(px):
        return (real_heigth * px) / pixels_heigth

    def width_px_to_cm(px):
        return (real_width * px) / pixels_width

    def height_cm_to_px(cm):
        return (pixels_height * cm) / real_height

    def width_cm_to_px(cm):
        return (pixels_width * cm) / real_width

    def rotate_point(pX, pY, oX, oY, angle):
        new_x = pX - oX
        new_y = pY - oY
        rotate_x = math.cos(math.radians(angle)) * new_x - math.sin(math.radians(angle)) * new_y
        rotate_y = math.sin(math.radians(angle)) * new_x + math.cos(math.radians(angle)) * new_y
        return (int(rotate_x + oX), int(rotate_y + oY))

NetworkTables.initialize(server='10.64.4.2')
time.sleep(1)
sb = NetworkTables.getTable('Shuffleboard')
map_table = sb.getSubTable('Map')
img = cv2.imread('quadra.PNG', 1)
cv2.imshow('sem modificar', img)
while True:
    quadra_modificada = img.copy() # reseta pra nao ficar 300 circulos na msm imagem
    x = map_table.getNumber('X', 0.0)
    y = map_table.getNumber('Y', 0.0)
    angle = map_table.getNumber('Angle', 0.0)
    xOrigin = int(utils.width_cm_to_px(real_width / 6))
    yOrigin = int(utils.height_cm_to_px(real_height) / 2) # origem da alianca azul
    xPoint = int(xOrigin + x)
    yPoint = int(yOrigin + y)
    lineX_start = xPoint + 30
    lineY_start = yPoint
    lineP1 = utils.rotate_point(lineX_start, lineY_start, xPoint, yPoint, angle)
    finalPoint = (xPoint, yPoint)
    cv2.circle(quadra_modificada, finalPoint, 10, (255, 0, 0), -1)
    cv2.line(quadra_modificada, finalPoint, lineP1, (0, 255, 0), 5)
    cv2.imshow('quadra modificada', quadra_modificada)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
