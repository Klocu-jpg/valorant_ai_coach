import cv2
import numpy as np

def analyze_crosshair(frame: np.ndarray) -> bool:
    # ROI around crosshair (center, small area)
    center_x, center_y = 960, 540
    crosshair_roi = frame[center_y-50:center_y+50, center_x-50:center_x+50]
    edges = cv2.Canny(cv2.cvtColor(crosshair_roi, cv2.COLOR_BGR2GRAY), 100, 200)
    
    # Rule-based: Bad if low edges (aiming at flat ground/wall), good if high edges (head level details)
    edge_count = np.sum(edges) / 255
    return edge_count < 100  # True if bad placement (threshold arbitrary, tune)