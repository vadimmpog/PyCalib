import numpy as np
import cv2 as cv
import imutils

chessboard_size = (6, 6)  # 9x6
file_path = 'F:\\Workspace\\CITIS_PROJECT\\VMS\\+-1\\MS_Record\\2021-10-06\\'
file_name = '+-1_20211006-160404_1_167.avi'

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

imgs = []

img_path = 'F:\\Workspace\\CITIS_PROJECT\\CalibPy\\cameras\\cam1\\frames\\2_+-1_20211006-161204_1_94.jpg'

# imgs = extractImages(file_path + file_name, file_path)
# for img in imgs:
img = cv.imread(img_path)
# h, w = img.shape[:2]
# print(w)
# img = cv.bilateralFilter(img,15,80,80)
# img = imutils.resize(img, width=2000)
# cv.imshow('img', img)
# cv.waitKey(5000)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Find the chess board corners
ret, corners = cv.findChessboardCorners(img, chessboard_size, None)
# If found, add object points, image points (after refining them)
print(ret)
if ret == True:
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    imgpoints.append(corners)
    # Draw and display the corners
    cv.drawChessboardCorners(img, chessboard_size, corners2, ret)
    cv.imshow('img', img)
    cv.waitKey(5000)
cv.destroyAllWindows()

# h, w = img.shape[:2]

# ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
#
# # undistort
# dst = cv.undistort(img, mtx, dist, None, newcameramtx)
#
# # crop the image
# x, y, w, h = roi
# dst = dst[y:y + h, x:x + w]
# cv.imwrite('calibresult.png', dst)

# mean_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
#     mean_error += error
# print( "total error: {}".format(mean_error/len(objpoints)) )
