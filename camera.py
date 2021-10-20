from calibrated_vid import CalibratedVid
import cv2 as cv


class Camera:
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    videos: list = []

    def __init__(self, cam_name) -> None:
        self.cam_name = cam_name
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def add_video(self, chessboard_size, file_path, vid_name):
        new_vid = CalibratedVid(chessboard_size, file_path, vid_name)
        self.videos.append(new_vid)

    def choose_frames(self):  ########
        vid: CalibratedVid
        all_frames = []
        for vid in self.videos:
            vid.extract_images()
            all_frames.append(vid.frames)

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
