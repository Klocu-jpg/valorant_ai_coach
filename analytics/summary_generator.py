from vod_learner.knowledge_updater import get_radiant_pct

def generate_summary(counts: dict, knowledge: dict) -> str:
    summary = "Post-Match Summary:\n"
    for key, value in counts.items():
        summary += f"{key.replace('_', ' ').title()}: {value}x\n"
    
    # Radiant benchmarks
    summary += "\nRadiant Benchmarks (from learned VODs):\n"
    for phase in ["early", "mid", "late"]:
        pct = get_radiant_pct(knowledge, phase)
        summary += f"{phase.title()} crosshair good: {pct:.0%}\n"
    
    focuses = ["Focus on matching Radiant crosshair placement"]
    summary += "\nMain Improvement Focuses:\n" + "\n".join(focuses)
    return summary