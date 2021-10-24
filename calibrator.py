import os
from imutils.video import FileVideoStream
import cv2 as cv
import numpy as np
import imutils


class Calibrator:
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    frames = [[], []]

    def __init__(self, cam_name, dir_path, chessboard_size=(7, 6)) -> None:
        self.cam_name = cam_name
        self.dir_path = dir_path
        self.chessboard_size = chessboard_size
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
        self.get_frames()

    def get_frames(self):
        img_path = f'{self.dir_path}\\cameras\\{self.cam_name}\\frames'
        self.frames[0].clear()
        self.frames[1].clear()
        for im_name in os.listdir(img_path):
            img = cv.imread(img_path+'\\'+im_name)
            self.frames[0].append(img)
            self.frames[1].append(im_name[:im_name.rfind('.')])

    def draw_corners(self, objpoints, imgpoints):
        for i in range(len(self.frames[0])):
            img = self.frames[0][i]
            # Find the chess board corners
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            ret, corners = cv.findChessboardCorners(img, self.chessboard_size, None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                path = f"{self.dir_path}\\cameras\\{self.cam_name}\\corners\\%s_corners.jpg" % (self.frames[1][i])
                if not os.path.isfile(path):
                    objpoints.append(self.objp)
                    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                    imgpoints.append(corners)
                    # Draw and display the corners
                    cv.drawChessboardCorners(img, self.chessboard_size, corners2, True)
                    # cv.imshow('Corners', img)
                    # cv.waitKey(1000)
                    cv.imwrite(path, img)
        # return objpoints, imgpoints

    def calibrate(self):
        h, w = img.shape[:2]
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    def undistort(self):
        path = f"{self.dir_path}\\cameras\\{self.cam_name}\\undistortions\\%s_undistortion.jpg" % (self.frames[1][i])
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv.imwrite(path, dst)

    def re_projection_error(self):
        mean_error = 0
        if self.mtx is not None:
            for i in range(len(self.objpoints)):
                imgpoints2, _ = cv.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist)
                error = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
                mean_error += error
            print("total error: {}".format(mean_error / len(self.objpoints)))

    def extract_images(self, path_in):
        frames = []
        count = 0
        fvs = FileVideoStream(path_in).start()
        while fvs.more():
            frame = fvs.read()
            if frame is not None:
                count += 1
                if count == 24:
                    # frame = imutils.resize(frame, width=450)
                    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    # frame = np.dstack([frame, frame, frame])
                    # cv.imshow('img', frame)
                    # cv.waitKey(5000)
                    frames.append(frame)
                    count = 0
        fvs.stop()
        return frames

    # def save_results
