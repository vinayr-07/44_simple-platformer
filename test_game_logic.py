from game.collision import swept_vertical_landing_y


def test_fast_fall_crossing_platform_lands():
    assert swept_vertical_landing_y(20, 90, 32, 50, 24, 0, 70, 200) == 70


def test_upward_motion_cannot_land():
    assert swept_vertical_landing_y(90, 20, 32, 50, 24, 0, 70, 200) is None


def test_no_land_without_horizontal_overlap():
    assert swept_vertical_landing_y(20, 90, 32, 220, 24, 0, 70, 200) is None
