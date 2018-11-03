import traceback
import sys
import time
import datetime

import cv2
import numpy as np

from .email import Notify
from .video import VideoWriter

DEBUG = True
DETECTION_THRESHOLD = 300


def detect_motion(prev, current):
    frame_diff = cv2.absdiff(prev, current)

    thresh_frame = cv2.threshold(
        frame_diff, 50, 255,
        cv2.THRESH_BINARY
    )[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    _, contours, _ = cv2.findContours(
        thresh_frame.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    contours = [(cv2.contourArea(c), c) for c in contours]
    contours = [c for c in contours if c[0] > DETECTION_THRESHOLD]

    if not contours:
        return

    max_contour = max(contours)[1]
    cv2.drawContours(thresh_frame, [max_contour], -1, (0, 255,0), 2)
    return max_contour


def main():
    capture = cv2.VideoCapture(0)
    movement_detected = False
    last_detected = time.time() - 10
    fails = 0
    try:
        time_count = time.time()
        previous_frame = None

        while True:
            ret, frame = capture.read()
            if not ret:
                fails += 1
                if fails > 5:
                    sys.exit()
                continue
            fails = 0

            gray = cv2.GaussianBlur(
                cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                ), (21, 21), 0)

            if previous_frame is None:
                previous_frame = gray
                continue

            contour = detect_motion(gray, previous_frame)
            should_notify = movement_detected is False
            movement_detected = contour is not None or (
                time.time() - last_detected < 5)

            if movement_detected:
                if should_notify:
                    Notify.notify(datetime.datetime.now())

                if contour is not None:
                    last_detected = time.time()
                    if DEBUG:
                        (x, y, w, h) = cv2.boundingRect(contour)
                        # making green rectangle arround the moving object
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                    (0, 255, 0), 3)

                cv2.putText(
                    frame, datetime.datetime.now().strftime("%m-%d-%y %I:%M:%S.%f %p"),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 0, 0), 1, cv2.LINE_AA
                )

                VideoWriter.write(frame)

            if DEBUG:
                pass
                # cv2.imshow("preview", frame)

            if cv2.waitKey(1):
                pass

            if time.time() - time_count > .5:
                previous_frame = gray
                time_count = time.time()

    finally:
        capture.release()
        VideoWriter.release()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
