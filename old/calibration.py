# Import required modules
import cv2
import numpy as np
import os
import glob
  
# Define the dimensions of checkerboard
CHECKERBOARD = (6, 4)
SIZE = 20 # mm

# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS + 
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
  
  
threedpoints = []
twodpoints = []  
#  3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] 
                      * CHECKERBOARD[1], 
                      3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                               0:CHECKERBOARD[1]].T.reshape(-1, 2)*SIZE
prev_img_shape = None

cap = cv2.VideoCapture(1)
found = 0
min_points=25

while(found < min_points):  # Here, 20 can be changed to whatever number you like to choose
    ret, image = cap.read() # Capture frame-by-frame
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    progress_message = "Points: "+str(len(twodpoints))+" of "+ str(min_points)
    cv2.putText(image, progress_message,
          (10, 30), cv2.FONT_HERSHEY_DUPLEX,
          1, (0, 255, 0), 2)

    ret, corners = cv2.findChessboardCorners(
                    grayColor, CHECKERBOARD, 
                    cv2.CALIB_CB_ADAPTIVE_THRESH 
                    + cv2.CALIB_CB_FAST_CHECK + 
                    cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret == True:
        threedpoints.append(objectp3d)
  
        # Refining pixel coordinates
        # for given 2d points.
        corners2 = cv2.cornerSubPix(
            grayColor, corners, (11, 11), (-1, -1), criteria)
  
        twodpoints.append(corners2)
  
        # Draw and display the corners
        image = cv2.drawChessboardCorners(image, 
                                          CHECKERBOARD, 
                                          corners2, ret)
        found += 1
        if len(twodpoints)==min_points:
            h, w = image.shape[:2]

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)
    cv2.imshow('img', image)
    cv2.waitKey(10)
  
cv2.destroyAllWindows()
# Displaying required output
print(" Camera matrix:")
print(np.array(matrix, dtype=np.int32))
  
print("\n Distortion coefficient:")
print(np.array(distortion, dtype=np.float16))



