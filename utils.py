import cv2
import numpy as np

def draw_text(image, text, position, color=(255, 255, 255), font_scale=0.8, thickness=2):
    """
    Draws text on an image with a black outline for better visibility.
    """
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness + 2)
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

def resize_frame(frame, width=640):
    """
    Resizes the frame to a specific width while maintaining aspect ratio.
    """
    h, w = frame.shape[:2]
    aspect_ratio = w / h
    new_height = int(width / aspect_ratio)
    return cv2.resize(frame, (width, new_height))
