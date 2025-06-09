def estimate_processing_time(duration_seconds, used_vosk):
    duration_min = duration_seconds / 60
    if used_vosk:
        return round(duration_min * 2.5)
    else:
        return round(duration_min * 0.6)