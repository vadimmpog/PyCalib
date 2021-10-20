import numpy as np
import cv2 as cv


class CalibratedVid:
    frames = []

    def __init__(self, file_path, file_name, chessboard_size) -> None:
        self.file_path = file_path
        self.file_name = file_name
        self.chessboard_size = chessboard_size
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1, 2)

    def extract_images(self, save=False, path_out=None):
        count = 0
        # images = []
        vidcap = cv.VideoCapture(self.file_path + '\\' + self.file_name)  # 333
        success, image = vidcap.read()
        success = True
        while success:
            vidcap.set(cv.CAP_PROP_POS_MSEC, (count * 1000))  # added this line
            self.frames.append(image)
            if save:
                cv.imwrite(path_out + "\\frame%d.jpg" % count, image)  # save frame as JPEG file
            success, image = vidcap.read()
            count = count + 1
        return count - 1

    def draw_corners(self, objpoints, imgpoints):
        for img in self.frames:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, self.chessboard_size, None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(self.objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv.drawChessboardCorners(img, self.chessboard_size, corners2, ret)
                # cv.imwrite(self.path_out + "\\corners%d.jpg" % count, img)
                # save corners!
        # cv.destroyAllWindows()
        return objpoints, imgpoints

    # def calibrate(self):
    #     h, w = img.shape[:2]
    #     ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
    #     newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    def undistort(self):
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv.imwrite('calibresult.png', dst)