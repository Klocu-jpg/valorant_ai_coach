import json
import os

KNOWLEDGE_PATH = "data/knowledge.json"

def load_knowledge() -> dict:
    if os.path.exists(KNOWLEDGE_PATH):
        with open(KNOWLEDGE_PATH, 'r') as f:
            return json.load(f)
    return {"phases": {"early": {"crosshair_good_count": 0, "total_count": 0},
                       "mid": {"crosshair_good_count": 0, "total_count": 0},
                       "late": {"crosshair_good_count": 0, "total_count": 0}}}

def save_knowledge(knowledge: dict):
    os.makedirs("data", exist_ok=True)
    with open(KNOWLEDGE_PATH, 'w') as f:
        json.dump(knowledge, f, indent=2)

def update_from_vod(phase_stats: dict):
    knowledge = load_knowledge()
    for phase, stats in phase_stats.items():
        if stats["total_count"] > 0:
            knowledge["phases"][phase]["crosshair_good_count"] += stats["crosshair_good_count"]
            knowledge["phases"][phase]["total_count"] += stats["total_count"]
    save_knowledge(knowledge)

def get_radiant_pct(knowledge: dict, phase: str) -> float:
    stats = knowledge["phases"][phase]
    return stats["crosshair_good_count"] / max(stats["total_count"], 1)