from game.collision import swept_vertical_landing_y
from game.level_data import DIFFICULTIES


def test_fast_fall_crossing_platform_lands():
    assert swept_vertical_landing_y(20, 90, 32, 50, 24, 0, 70, 200) == 70


def test_upward_motion_cannot_land():
    assert swept_vertical_landing_y(90, 20, 32, 50, 24, 0, 70, 200) is None


def test_no_land_without_horizontal_overlap():
    assert swept_vertical_landing_y(20, 90, 32, 220, 24, 0, 70, 200) is None


def test_each_difficulty_has_a_distinct_scenario():
    scenarios = [difficulty["scenario"] for difficulty in DIFFICULTIES]
    layouts = [difficulty["platforms"] for difficulty in DIFFICULTIES]

    assert len(set(scenarios)) == 3
    assert len(set(layouts)) == 3


def test_difficulty_layouts_have_valid_goals_and_platforms():
    for difficulty in DIFFICULTIES:
        assert 0 < difficulty["goal_x"] < 800
        assert difficulty["platforms"]
        assert difficulty["platforms"][0][0] == 0
        assert all(width > 0 and height > 0 for _, _, width, height in difficulty["platforms"])
