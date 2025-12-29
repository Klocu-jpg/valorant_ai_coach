import cv2
from vision.timer_reader import read_timer
from vision.minimap_analyzer import analyze_minimap
from vision.crosshair_analyzer import analyze_crosshair
from logic.round_phase import get_round_phase
from vision.movement_analyzer import MovementAnalyzer

def analyze_vod_frames(video_path: str) -> dict:
    """
    Extract ~1 frame/sec, analyze only valid Valorant frames.
    Returns phase_stats: {phase: {'crosshair_good_count': int, 'total_count': int}}
    """
    cap = cv2.VideoCapture(video_path)
    movement = MovementAnalyzer()
    
    phase_stats = {"early": {"crosshair_good_count": 0, "total_count": 0},
                   "mid": {"crosshair_good_count": 0, "total_count": 0},
                   "late": {"crosshair_good_count": 0, "total_count": 0}}
    
    frame_interval = 30  # ~1/sec at 30fps
    count = 0
    valid_frames = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if count % frame_interval != 0:
            count += 1
            continue
        
        timer = read_timer(frame)
        if timer is None:
            count += 1
            continue
        
        minimap_info = analyze_minimap(frame)
        if not minimap_info["player_visible"]:
            count += 1
            continue
        
        # Valid frame
        valid_frames += 1
        phase = get_round_phase(timer)
        crosshair_bad = analyze_crosshair(frame)
        movement_info = movement.analyze_movement(frame)
        
        # Only count crosshair for stats (expandable)
        stats = phase_stats[phase]
        stats["total_count"] += 1
        if not crosshair_bad:
            stats["crosshair_good_count"] += 1
        
        count += 1
    
    cap.release()
    print(f"Analyzed {valid_frames} valid frames from VOD.")
    return phase_stats