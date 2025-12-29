import time
import cv2
import time
import threading
from screen_capture.capture import ScreenCapturer
from vision.timer_reader import read_timer
from vision.minimap_analyzer import analyze_minimap
from vision.crosshair_analyzer import analyze_crosshair
from vision.movement_analyzer import MovementAnalyzer
from logic.round_phase import get_round_phase
from logic.decision_windows import DecisionWindowManager
from logic.radiant_patterns import get_radiant_pattern
from analytics.mistake_tracker import MistakeTracker
from analytics.summary_generator import generate_summary
from coach.live_callouts import make_callout
from coach.confidence_score import calculate_confidence
from ui.main_window import CoachGUI
from ui.match_summary_window import show_summary
from ui.main_window import CoachGUI  # But inline loop
from vod_learner.knowledge_updater import load_knowledge

def coaching_loop(knowledge):  # Extracted for GUI
    capturer = ScreenCapturer()
    movement_analyzer = MovementAnalyzer()
    decision_manager = DecisionWindowManager()
    tracker = MistakeTracker()
    
    match_ongoing = True
    while match_ongoing:  # Ctrl+C to end
        frame = capturer.capture_frame()
        time_seconds = read_timer(frame)
        phase = get_round_phase(time_seconds)
        
        minimap_info = analyze_minimap(frame)
        crosshair_bad = analyze_crosshair(frame)
        movement_info = movement_analyzer.analyze_movement(frame)
        
        tracker.update(crosshair_bad, movement_info, time_seconds or 0)
        
        if decision_manager.is_decision_window_open():
            suggestion = get_radiant_pattern(phase, crosshair_bad, knowledge)  # Updated!
            if suggestion:
                confidence = calculate_confidence(phase, minimap_info)
                make_callout(suggestion, confidence, knowledge)  # Updated
        
        time.sleep(0.1)
    
    summary = generate_summary(tracker.counts, knowledge)  # Updated
    show_summary(summary)

if __name__ == "__main__":
    # For GUI integration, but MVP: GUI calls coaching_loop
    gui = CoachGUI()
    # In CoachGUI.coaching_loop: coaching_loop(gui.knowledge)