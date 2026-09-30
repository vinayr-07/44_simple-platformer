import io
import math
import struct
import wave

import pygame


class SoundManager:
    """Generate lightweight jump, goal, and death effects without asset files."""

    SAMPLE_RATE = 22050

    def __init__(self):
        self.enabled = False
        self.jump = None
        self.goal = None
        self.death = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=self.SAMPLE_RATE, size=-16, channels=1, buffer=512)
            self.jump = self._make_tone(((660, 0.08), (880, 0.10)))
            self.goal = self._make_tone(((523, 0.10), (659, 0.10), (784, 0.16)))
            self.death = self._make_tone(((392, 0.12), (330, 0.12), (262, 0.22)))
            self.enabled = True
        except pygame.error:
            pass

    def _make_tone(self, notes):
        samples = []
        for frequency, duration in notes:
            count = int(self.SAMPLE_RATE * duration)
            attack = max(1, int(self.SAMPLE_RATE * 0.01))
            release = max(1, int(self.SAMPLE_RATE * 0.03))
            for index in range(count):
                t = index / self.SAMPLE_RATE
                envelope = min(1.0, index / attack)
                envelope *= min(1.0, (count - index) / release)
                value = int(12000 * envelope * math.sin(2 * math.pi * frequency * t))
                samples.append(struct.pack("<h", value))

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            wav_file.writeframes(b"".join(samples))
        buffer.seek(0)
        return pygame.mixer.Sound(file=buffer)

    def _play(self, sound):
        if self.enabled and sound is not None:
            sound.play()

    def play_jump(self):
        self._play(self.jump)

    def play_goal(self):
        self._play(self.goal)

    def play_death(self):
        self._play(self.death)
