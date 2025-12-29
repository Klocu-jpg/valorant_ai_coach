from vod_learner.knowledge_updater import get_radiant_pct

def get_radiant_pattern(phase: str, crosshair_bad: bool, knowledge: dict) -> str | None:
    if crosshair_bad and phase in knowledge["phases"]:
        pct = get_radiant_pct(knowledge, phase)  # Import from knowledge_updater if needed
        if pct > 0.6:  # Learned benchmark
            return f"Radiants hit head-level crosshair {pct:.0%} in {phase} rounds – preaim there"
    # Fallback rules
    if phase == "early":
        return "Hold your off-angle patiently"
    # ... (keep originals)
    return None