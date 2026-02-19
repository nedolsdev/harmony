"""Create a hex sprite surface."""

import math

import pygame


def create_hex_sprite(
    radius: int,
    color: tuple[int, int, int],
    outline_color: tuple[int, int, int] = (0, 0, 0),
) -> pygame.Surface:
    """Create a hex sprite surface."""
    width = int(math.sqrt(3) * radius)
    height = int(2 * radius)

    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    cx = width / 2
    cy = height / 2

    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)  # -30 makes it pointy-top
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, outline_color, points, 2)

    return surface
