from audio.tts import speak
from vod_learner.knowledge_updater import get_radiant_pct  # For dynamic

def make_callout(suggestion: str, confidence: float, knowledge: dict):
    if confidence > 0.7:
        speak(suggestion)