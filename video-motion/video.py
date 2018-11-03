import os
import datetime
import cv2
import shutil

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


class VideoWriter(object):
    writer = None
    day = datetime.datetime.today().strftime("%m_%d_%y")

    @classmethod
    def write(cls, frame):
        today = datetime.datetime.today().strftime("%m_%d_%y")
        if cls.writer is None or cls.day != today:
            file_name = datetime.datetime.today().strftime("%m_%d_%y-%I:%M:%S.%p")
            path = os.path.join(OUTPUT_DIR, f"{file_name}.avi")
            cls.day = today
            cls.writer = cv2.VideoWriter(
                path,
                cv2.VideoWriter_fourcc(*"XVID"),
                20.0, (640, 480)
            )
        cls.writer.write(frame)

    @classmethod
    def release(cls):
        if cls.writer is not None:
            cls.writer.release()
