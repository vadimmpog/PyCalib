import os
from PyQt5.QtCore import QObject, pyqtSignal
from imutils.video import FileVideoStream
import cv2 as cv
import numpy as np
import imutils
import pickle


class Calibrator(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, cam_name, dir_path, chessboard_size=(7, 6)) -> None:
        self.frames = [[], []]
        super().__init__()
        self.cam_name = cam_name
        self.dir_path = dir_path
        self.chessboard_size = chessboard_size
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
        self.file_name = f'{self.dir_path}\\cameras\\{self.cam_name}\\results'

    def get_frames(self):
        img_path = f'{self.dir_path}\\cameras\\{self.cam_name}\\frames'
        self.frames[0].clear()
        self.frames[1].clear()
        for im_name in os.listdir(img_path):
            img = cv.imread(img_path + '\\' + im_name)
            self.frames[0].append(img)
            self.frames[1].append(im_name[:im_name.rfind('.')])

    def get_results(self):
        if not os.path.exists(self.file_name):
            open(self.file_name, "x").close()
        open_file = open(self.file_name, "rb")
        try:
            self.error, self.main_results = pickle.load(open_file)
            if not self.main_results:
                self.main_results, self.error = [], 1
        except EOFError:
            self.main_results, self.error = [], 1
        open_file.close()

    def save_results(self):
        open_file = open(self.file_name, "wb")
        pickle.dump([self.error, self.main_results], open_file)
        open_file.close()

    def start(self):
        for i in range(len(self.frames[0])):
            # print('i', i, len(self.frames[0]), self.frames[1][0], self.cam_name)
            img = self.frames[0][i]
            # Find the chess board corners
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            ret, corners = cv.findChessboardCorners(img, self.chessboard_size, None)
            # If found, add object points, image points (after refining them)
            if ret:
                objpoints, imgpoints = self.draw_corners(i, img, gray, corners)
                if objpoints is not None:

                    results = self.calibrate(objpoints, imgpoints, img, gray)

                    error = self.re_projection_error(objpoints, imgpoints, results[0], results[1], results[2], results[3])
                    if error < self.error:
                        self.error = error
                        self.main_results = results

            self.progress.emit(i + 1)
        x = len(self.frames[0]) + 1

        if self.main_results:
            for i in range(len(self.frames[0])):
                img = self.frames[0][i]
                self.undistort(i, img, self.main_results[0], self.main_results[1], self.main_results[4], self.main_results[5])
                self.progress.emit(x + i + 1)
            self.save_results()

        self.finished.emit()

    def draw_corners(self, i, img, gray, corners):
        objpoints = []
        imgpoints = []
        path = f"{self.dir_path}\\cameras\\{self.cam_name}\\corners\\%s_corners.jpg" % (self.frames[1][i])
        if not os.path.isfile(path):
            objpoints.append(self.objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            imgpoints.append(corners)
            cv.drawChessboardCorners(img, self.chessboard_size, corners2, True)
            cv.imwrite(path, img)
            return objpoints, imgpoints
        else:
            return None, None

    def calibrate(self, objpoints, imgpoints, img, gray):
        h, w = img.shape[:2]
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        if ret:
            return [mtx, dist, rvecs, tvecs, newcameramtx, roi]

    def undistort(self, i, img, mtx, dist, newcameramtx, roi, crop=False):
        path = f"{self.dir_path}\\cameras\\{self.cam_name}\\undistortions\\%s_undistortion.jpg" % (self.frames[1][i])
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # crop the image
        if crop:
            x, y, w, h = roi
            dst = dst[y:y + h, x:x + w]
        cv.imwrite(path, dst)

    def re_projection_error(self, objpoints, imgpoints, mtx, dist, rvecs, tvecs):
        mean_error = 0
        if mtx is not None:
            for i in range(len(objpoints)):
                imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
                error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
                mean_error += error
        return mean_error / len(objpoints)

    def extract_images(self, path_in):
        frames = []
        count = 0
        fvs = FileVideoStream(path_in).start()
        while fvs.more():
            frame = fvs.read()
            if frame is not None:
                count += 1
                if count == 24:
                    frame = imutils.resize(frame, width=900)
                    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    # frame = np.dstack([frame, frame, frame])
                    frames.append(frame)
                    count = 0
        fvs.stop()
        return frames

