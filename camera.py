import cv2 as cv
import numpy as np


class Camera:
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    videos: list = []
    frames: list = []

    def __init__(self, cam_name, chessboard_size=(7, 6)) -> None:
        self.cam_name = cam_name
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)



    # def add_video(self, chessboard_size, file_path, vid_name):
    #     new_vid = CalibratedVid(chessboard_size, file_path, vid_name)
    #     self.videos.append(new_vid)

    # def choose_frames(self):  ########
    #     all_frames = []
    #     for vid in self.videos:
    #         vid.extract_images()
    #         all_frames.append(vid.frames)

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

    # def undistort(self):
    #     dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    #     # crop the image
    #     x, y, w, h = roi
    #     dst = dst[y:y + h, x:x + w]
    #     cv.imwrite('calibresult.png', dst)

    def get_calib_res(self):
        return self.ret, self.mtx, self.dist, self.rvecs, self.tvecs

    def re_projection_error(self):
        mean_error = 0
        if self.mtx is not None:
            for i in range(len(self.objpoints)):
                imgpoints2, _ = cv.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist)
                error = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
                mean_error += error
            print("total error: {}".format(mean_error / len(self.objpoints)))
