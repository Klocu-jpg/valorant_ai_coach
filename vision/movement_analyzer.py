import cv2
import numpy as np

class MovementAnalyzer:
    def __init__(self):
        self.prev_frame = None

    def analyze_movement(self, frame: np.ndarray) -> dict:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_frame is None:
            self.prev_frame = gray
            return {"peeking": False, "repositioning": False}
        
        # Optical flow for movement detection
        flow = cv2.calcOpticalFlowFarneback(self.prev_frame, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        # Rule-based: High magnitude on edges = peeking
        peeking = np.mean(mag) > 5  # Threshold for peek movement
        repositioning = np.mean(mag) < 2 and peeking  # Low after high = reposition (simplified)
        
        self.prev_frame = gray
        return {"peeking": peeking, "repositioning": repositioning}