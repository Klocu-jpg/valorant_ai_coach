import cv2
import numpy as np

def analyze_minimap(frame: np.ndarray) -> dict:
    # ROI for minimap (bottom left, assuming 1920x1080)
    minimap_roi = frame[900:1080, 0:200]
    hsv = cv2.cvtColor(minimap_roi, cv2.COLOR_BGR2HSV)
    
    # Simple rule-based: Detect player icon (blue-ish) and enemies (red-ish)
    player_mask = cv2.inRange(hsv, np.array([90, 50, 50]), np.array([130, 255, 255]))  # Blue for player
    enemy_mask = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))  # Red for enemies
    
    player_pos = cv2.countNonZero(player_mask) > 10  # True if player icon detected
    enemies_near = cv2.countNonZero(enemy_mask) > 5  # Rough count of red blobs
    
    return {
        "player_visible": player_pos,
        "enemies_near": enemies_near
    }