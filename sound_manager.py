# sound_manager.py - Manages game sounds

import pygame
import math
from array import array

class SoundManager:
    """Manages game sounds (Single Responsibility: sound handling)."""
    def __init__(self):
        self.ai_sound = self._make_tone(880, duration_ms=90, volume=0.18)
        self.player_sound = self._make_tone(660, duration_ms=80, volume=0.2)

    def _make_tone(self, freq_hz, duration_ms=120, volume=0.18, samplerate=44100):
        """Generate a soft click tone (Encapsulation: internal method)."""
        length = int(samplerate * (duration_ms / 1000.0))
        amplitude = int(32767 * volume)
        data = array('h')
        for i in range(length):
            t = i / samplerate
            sample = math.sin(2 * math.pi * freq_hz * t)
            env = (i / length) if i < length * 0.1 else (1 - ((i - length * 0.1) / (length * 0.9)))**2
            env = max(0.0, min(1.0, env))
            data.append(int(amplitude * sample * env))
        return pygame.mixer.Sound(buffer=data)

    def play_ai(self):
        self.ai_sound.play()

    def play_player(self):
        self.player_sound.play()