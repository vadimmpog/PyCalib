import numpy as np
import cv2 as cv

chessboard_size = (7, 6)  # 9x6
file_path = 'E:\\Workspace\\CALIB\\VMS\\+-1\\MS_Record\\2021-10-06\\cam1\\'
file_name = '+-1_20211006-160404_1_167.avi'

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

imgs = []


def extractImages(path_in, save=False, path_out=None):
    count = 0
    frames = []
    vidcap = cv.VideoCapture(path_in)
    success, image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv.CAP_PROP_POS_MSEC, (count * 1000))  # added this line
        frames.append(image)
        # cv.imwrite(pathOut + "\\frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count = count + 1
    return frames


# img_path = 'E:\\Workspace\\CITIS\\Screenshot_5.png'

imgs = extractImages(file_path + file_name, file_path)
for img in imgs:
    # img = cv.imread(img_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboard_size, corners2, ret)
        # cv.imshow('img', img)
        # cv.waitKey(5000)
cv.destroyAllWindows()

h, w = img.shape[:2]

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
cv.imwrite('calibresult.png', dst)

# mean_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
#     mean_error += error
# print( "total error: {}".format(mean_error/len(objpoints)) )
