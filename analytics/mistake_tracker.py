class MistakeTracker:
    def __init__(self):
        self.counts = {
            "bad_crosshair": 0,
            "bad_peek": 0,
            "repeek_no_info": 0,
            "overexposure": 0,
            "good_patience": 0,
            "good_repositioning": 0
        }
        self.last_peek_time = 0

    def update(self, crosshair_bad: bool, movement_info: dict, time_seconds: int):
        if crosshair_bad:
            self.counts["bad_crosshair"] += 1
        if movement_info["peeking"]:
            self.counts["bad_peek"] += 1  # Assume all peeks bad for MVP; refine later
            if time.time() - self.last_peek_time < 5:  # Repeek within 5s
                self.counts["repeek_no_info"] += 1
            self.last_peek_time = time.time()
        if movement_info["peeking"] and time_seconds < 30:  # Overexposure late
            self.counts["overexposure"] += 1
        if not movement_info["peeking"] and time_seconds > 90:
            self.counts["good_patience"] += 1
        if movement_info["repositioning"]:
            self.counts["good_repositioning"] += 1