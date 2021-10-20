from calibrated_vid import CalibratedVid


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

    def calibrate(self):    ########
        vid: CalibratedVid
        for vid in self.videos:
            vid.extract_images()
