#-​*- coding: UTF-8 -*​-
# coding=gbk

import cv2
import numpy as np
import pysrt

class FrameHistCalculator(object):

    def __init__(self, sub_end_diff=350, video_backward_diff=400):
        self.sub_end_diff = sub_end_diff
        self.video_backward_diff = video_backward_diff

    # end of subtitle in seconds
    def get_sub_end_time(self, subtitle_path):
        subtitle = pysrt.open(subtitle_path)
        end_of_sub = subtitle[-1].end
        end_time = self.transformToSeconds(end_of_sub.hours, end_of_sub.minutes, end_of_sub.seconds, end_of_sub.milliseconds)
        return end_time

    def transform_to_seconds(swelf, hour, minute, seconds, milliseconds):
        result = ((((hour * 60) + minute) * 60) + seconds) + (float(milliseconds) / 1000)
        return result

    # return a bool to when provided with a frame
    def frame_histpolarization(self, frame):
        hist_numpy, bins = np.histogram(frame.ravel(),256,[0,256])

        # try to find the most dominating color in hist and calculate its precentange
        sorted_hist = np.sort(hist_numpy)
        polarized_pixel = sum(sorted_hist[-5 :])
        total_pixel_count = sum(hist_numpy)
        return float(polarized_pixel) / total_pixel_count

    def is_credit(self, blackNwhite_ratio, credit_buffer):
        credit_buffer.append(blackNwhite_ratio)
        credit_buffer.popleft()
        # print credit_buffer
        return credit_buffer

    # return a bool to when provided with a frame
    def frame_hist_polarization(self, frame):
        hist_numpy, bins = np.histogram(frame.ravel(),256,[0,256])

        # black and white approach but fail on some other colors
        # black_pixel_count = sum(hist_numpy[0: 3])
        # white_pixel_count = sum(hist_numpy[-3: ])

        # try to find the most dominating color in hist and calculate its precentange
        sorted_hist = np.sort(hist_numpy)
        polarized_pixel = sum(sorted_hist[-5 :])
        total_pixel_count = sum(hist_numpy)
        return float(polarized_pixel) / total_pixel_count

    def video_reader(self, video_path):
        #read video and get video parameters
        cap = cv2.VideoCapture(video_path.encode("utf8"))
        self.length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        self.fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.cap = cap

    def set_timestamp(self, start_frame, skipping_frame=20):
        num_frame = self.data_array.shape[0]
        step = int(skipping_frame/self.fps * 10**6)
        start_time = int(start_frame/self.fps * 10**6)
        timestamp = [start_time + x *step for x in range(num_frame)]
        return timestamp

    def get_start_frame(self, subtitle_path):
        # get process end time from either end of video 
        # or end of subtitle(cautious to use subtitle)
        if subtitle_path == None:
            end_of_video = self.length / self.fps
        else:
            subtitle = pysrt.open(subtitle_path)
            self.end_of_video = self.get_sub_end_time(subtitle)

        #get a start index to process
        if ((self.length / self.fps) - end_of_video) > self.sub_end_diff:
            frame_number_start = int(end_of_video * self.fps)

        else:
            frame_number_start = int(self.length - (self.video_backward_diff *self.fps))

        return frame_number_start

    def frame_hist_calculation(self, start_time, skipping_number=20):
        frame_index = start_time
        hist_res = []
        while(self.cap.isOpened() and frame_index < self.length):
            self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = self.cap.read()
            if not frame.any() : break
            ratio = self.fram_hist_polarization(frame)
            hist_res.append(ratio)
            frame_index += skipping_number

        self.data_array = np.asarray(hist_res)
        return self.data_array



