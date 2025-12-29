def calculate_confidence(phase: str, minimap_info: dict) -> float:
    # Simple: High if phase known and minimap has info
    if phase != "unknown" and minimap_info["player_visible"]:
        return 0.8
    return 0.5