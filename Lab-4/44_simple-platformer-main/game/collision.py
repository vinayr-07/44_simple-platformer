def swept_vertical_landing_y(
    previous_y: float,
    next_y: float,
    player_height: int,
    player_x: float,
    player_width: int,
    platform_x: int,
    platform_y: int,
    platform_width: int,
) -> float | None:
    """Return the platform top if the player's downward path crosses it."""
    if next_y < previous_y:
        return None

    horizontal_overlap = (
        player_x + player_width > platform_x
        and player_x < platform_x + platform_width
    )
    if not horizontal_overlap:
        return None

    previous_bottom = previous_y + player_height
    next_bottom = next_y + player_height
    if previous_bottom <= platform_y <= next_bottom:
        return float(platform_y)
    return None
