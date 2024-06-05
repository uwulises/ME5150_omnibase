#importar librerias para deteccion de aruco
import cv2 as cv
import numpy as np
import os 
import sys
import cv2.aruco 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../herramientas')))

from aruco import ArucoHunting
from shape_detector import ShapeDetector

cap=cv.VideoCapture(1)
hunter = ArucoHunting()
hunter.set_marker_length(0.03) # en metros
#calibración de la cámara para usar en la funcion set_camera_parameters
camera_matrix = np.array([[787., 0., 299.],[0., 782., 233.],[0., 0., 1.]])
dist_coeff = np.array([[-3.230e-01, -2.236e+00,  3.409e-02,  3.244e-03,  8.758e+00]])
hunter.set_camera_parameters(camera_matrix, dist_coeff)

while cap.isOpened():
    ret, frame = cap.read()
    hunter.update_image(frame)
    hunter.update_pose_and_corners()
    aruco_pose = hunter.pose
    aruco_corners = hunter.corners
    aruco_ids = hunter.ids
    print(aruco_pose)

    #dibujar los marcadores detectados
    if aruco_ids is not None and len(aruco_ids) > 0:
        cv2.aruco.drawDetectedMarkers(frame, aruco_corners, aruco_ids)
                

    # Mostrar la imagen en una ventana
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


