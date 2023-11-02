#importar librerias para deteccion de aruco
import cv2 as cv
import numpy as np
import os 
import sys
import time
import cv2
from cv2 import aruco
current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_directory, '../herramientas'))
sys.path.append(os.path.join(current_directory, '../src'))
sys.path.append(os.path.join(current_directory, '..'))
from client.omnibase_robot_client import RobotClient
from aruco import ArucoHunting

robot = RobotClient("omni.local")

cap=cv2.VideoCapture(1)
hunter = ArucoHunting()
hunter.set_marker_length(0.03) # en metros
#calibración de la cámara para usar en la funcion set_camera_parameters
# camera_matrix = 
# dist_coeff = 
#hunter.set_camera_parameters(camera_matrix, dist_coeff)

while cap.isOpened():
    ret, frame = cap.read()
    hunter.update_image(frame)
    hunter.update_pose_and_corners()
    aruco_pose = hunter.pose
    aruco_corners = hunter.corners
    aruco_ids = hunter.ids

    #se aplica un contador para printear solo algunos frames
    counter=0
    #dibujar los marcadores detectados
    if counter%100==0:
        if aruco_ids is not None and len(aruco_ids) > 0:
            cv2.aruco.drawDetectedMarkers(frame, aruco_corners, aruco_ids)
            #se agrega movimiento dependiendo del id del marcador usando un diccionario
            #asignar movimientos a los id
            robot.send_move_command("movimientos")

    # Mostrar la imagen en una ventana
    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        robot.send_move_command('stop')
        break

cap.release()
cv2.destroyAllWindows()
