"""Difficulty-specific level configurations for the platformer."""

DIFFICULTIES = (
    {
        "name": "Easy",
        "scenario": "Training Meadow",
        "gravity": 0.42,
        "jump_strength": -11.5,
        "speed": 4.5,
        "max_fall_speed": 13.0,
        "goal_x": 700,
        "background": (116, 178, 232),
        # (x, y offset from ground, width, height)
        "platforms": (
            (0, 0, 210, 14),
            (230, 0, 150, 14),
            (400, -50, 170, 14),
            (590, -20, 150, 14),
        ),
        # (x, platform y offset from ground, width, height)
        "hazards": (
            (300, 0, 36, 14),
        ),
    },
    {
        "name": "Medium",
        "scenario": "Bridge Run",
        "gravity": 0.60,
        "jump_strength": -12.0,
        "speed": 4.0,
        "max_fall_speed": 15.0,
        "goal_x": 740,
        "background": (100, 160, 220),
        "platforms": (
            (0, 0, 160, 14),
            (220, 0, 140, 14),
            (420, -60, 120, 14),
            (600, 0, 180, 14),
        ),
        "hazards": (
            (240, 0, 100, 14),
        ),
    },
    {
        "name": "Hard",
        "scenario": "Sky Gauntlet",
        "gravity": 0.80,
        "jump_strength": -13.5,
        "speed": 4.0,
        "max_fall_speed": 17.0,
        "goal_x": 775,
        "background": (68, 108, 168),
        "platforms": (
            (0, 0, 140, 14),
            (180, -40, 110, 14),
            (330, -90, 105, 14),
            (475, -30, 110, 14),
            (625, -80, 100, 14),
            (755, 0, 45, 14),
        ),
        "hazards": (
            (205, -40, 28, 14),
            (350, -90, 25, 14),
            (500, -30, 28, 14),
        ),
    },
)
