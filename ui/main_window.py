import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import json
from vod_learner.downloader import download_vod
from vod_learner.frame_analyzer import analyze_vod_frames
from vod_learner.knowledge_updater import update_from_vod, load_knowledge
from .match_summary_window import show_summary
# Import main loop parts (refactored below)

class CoachGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Valorant AI Coach")
        self.root.geometry("400x300")
        self.knowledge = load_knowledge()
        
        tk.Label(self.root, text="Valorant AI Coach\n(Learns from Radiant VODs!)", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Learn from Radiant VOD", command=self.learn_vod, bg="green", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Start Live Coaching", command=self.start_coaching, bg="blue", font=("Arial", 12)).pack(pady=10)
        
        self.status = tk.Label(self.root, text="Ready", fg="green")
        self.status.pack(pady=20)
        
        self.root.mainloop()
    
    def learn_vod(self):
        url = simpledialog.askstring("Learn VOD", "Enter Radiant VOD YouTube URL:\n(e.g., https://www.youtube.com/watch?v=UmM7F7T5fP4)")
        if not url:
            return
        
        self.status.config(text="Downloading...", fg="orange")
        self.root.update()
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                video_path = download_vod(url, temp_dir)
                phase_stats = analyze_vod_frames(video_path)
                update_from_vod(phase_stats)
                self.knowledge = load_knowledge()  # Reload
            self.status.config(text="Learned! Knowledge updated.", fg="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Failed", fg="red")
    
    def start_coaching(self):
        self.root.withdraw()  # Hide GUI
        # Run coaching in thread to allow summary later
        thread = threading.Thread(target=self.coaching_loop)
        thread.start()
        thread.join()  # Wait for end
        self.root.deiconify()  # Show back if needed
    
    def coaching_loop(self):
        def main():
            capturer = ScreenCapturer()
            movement_analyzer = MovementAnalyzer()
            decision_manager = DecisionWindowManager()
            tracker = MistakeTracker()
    
            match_ongoing = True  # For MVP, run until Ctrl+C; in future, detect match end via OCR on score
            while match_ongoing:
                frame = capturer.capture_frame()
                time_seconds = read_timer(frame)
                phase = get_round_phase(time_seconds)
                
                minimap_info = analyze_minimap(frame)
                crosshair_bad = analyze_crosshair(frame)
                movement_info = movement_analyzer.analyze_movement(frame)
                
                tracker.update(crosshair_bad, movement_info, time_seconds or 0)
                
                if decision_manager.is_decision_window_open():
                    suggestion = get_radiant_pattern(phase, minimap_info)
                    if suggestion:
                        confidence = calculate_confidence(phase, minimap_info)
                        make_callout(suggestion, confidence)
                
                time.sleep(0.1)  # ~10 FPS to avoid CPU overload
    
    # After match (manual stop for MVP)
    summary = generate_summary(tracker.counts)
    show_summary(summary)

# For now, integrate in main.py