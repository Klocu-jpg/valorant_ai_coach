import time

class DecisionWindowManager:
    def __init__(self):
        self.last_decision_time = 0
        self.window_interval = 10  # Seconds between decisions

    def is_decision_window_open(self) -> bool:
        current_time = time.time()
        if current_time - self.last_decision_time > self.window_interval:
            self.last_decision_time = current_time
            return True
        return False