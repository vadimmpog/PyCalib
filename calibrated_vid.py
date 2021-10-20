import numpy as np
import cv2 as cv


class CalibratedVid:
    frames = []

    def __init__(self, file_path, file_name, chessboard_size) -> None:
        self.file_path = file_path
        self.file_name = file_name
        self.chessboard_size = chessboard_size

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
            # img = cv.imread(img_path)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, self.chessboard_size, None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                cv.drawChessboardCorners(img, self.chessboard_size, corners2, ret)

                # cv.imshow('img', img)
                # cv.waitKey(5000)
        cv.destroyAllWindows()
        return objpoints, imgpoints
