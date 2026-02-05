"""Sound effects for Quiz Master using system beeps."""

import sys

# Try to import platform-specific sound modules
if sys.platform == "win32":
    import winsound
    SOUND_AVAILABLE = True
else:
    SOUND_AVAILABLE = False

# Sound enabled flag (can be toggled by user)
_sound_enabled = True


def set_sound_enabled(enabled: bool):
    """Enable or disable sound effects."""
    global _sound_enabled
    _sound_enabled = enabled


def is_sound_enabled() -> bool:
    """Check if sound is enabled."""
    return _sound_enabled and SOUND_AVAILABLE


def play_beep(frequency: int, duration: int):
    """Play a beep at given frequency (Hz) and duration (ms)."""
    if not is_sound_enabled():
        return
    try:
        if sys.platform == "win32":
            winsound.Beep(frequency, duration)
    except Exception:
        pass  # Silently fail if sound doesn't work


def play_correct():
    """Play sound for correct answer - ascending happy tone."""
    if not is_sound_enabled():
        return
    try:
        play_beep(523, 100)  # C5
        play_beep(659, 100)  # E5
        play_beep(784, 150)  # G5
    except Exception:
        pass


def play_wrong():
    """Play sound for wrong answer - descending sad tone."""
    if not is_sound_enabled():
        return
    try:
        play_beep(392, 150)  # G4
        play_beep(311, 200)  # Eb4
    except Exception:
        pass


def play_countdown():
    """Play countdown tick sound."""
    if not is_sound_enabled():
        return
    try:
        play_beep(440, 80)  # A4 - short tick
    except Exception:
        pass


def play_start():
    """Play game start sound - fanfare."""
    if not is_sound_enabled():
        return
    try:
        play_beep(523, 100)  # C5
        play_beep(523, 100)  # C5
        play_beep(523, 100)  # C5
        play_beep(659, 300)  # E5 (longer)
    except Exception:
        pass


def play_win():
    """Play victory sound."""
    if not is_sound_enabled():
        return
    try:
        play_beep(523, 100)  # C5
        play_beep(587, 100)  # D5
        play_beep(659, 100)  # E5
        play_beep(698, 100)  # F5
        play_beep(784, 200)  # G5
        play_beep(1047, 300) # C6
    except Exception:
        pass


def play_menu_select():
    """Play menu selection sound."""
    if not is_sound_enabled():
        return
    try:
        play_beep(600, 50)
    except Exception:
        pass


def play_timer_warning():
    """Play urgent timer warning sound."""
    if not is_sound_enabled():
        return
    try:
        play_beep(880, 100)  # A5 - urgent
        play_beep(880, 100)  # A5
    except Exception:
        pass
