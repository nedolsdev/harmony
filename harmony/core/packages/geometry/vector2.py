"""Defines a 2D float Vector."""

from __future__ import annotations

import math
from typing import Self, overload


class Vector2:  # noqa: PLW1641 (unhashable)
    """Defines a 2D float Vector."""

    # just a performance thing (info: https://stackoverflow.com/questions/472000/usage-of-slots)
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """Initialize the 2D Vector."""
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        """Get debugging representation."""
        return f"Vector2(x={self.x:.4f}, y={self.y:.4f})"

    def perpendicular(self) -> Vector2:
        """Return a perpendicular vector (rotated 90 degrees CCW)."""
        return Vector2(-self.y, self.x)

    def perpendicular_cw(self) -> Vector2:
        """Return a perpendicular vector (rotated 90 degrees CW)."""
        return Vector2(self.y, -self.x)

    def __str__(self) -> str:
        """Get string representation."""
        return f"({self.x}, {self.y})"

    def copy(self) -> Vector2:
        """Create a copy of the Vector."""
        return Vector2(self.x, self.y)

    def as_tuple(self) -> tuple[float, float]:
        """Return the Vector as a tuple."""
        return self.x, self.y

    def as_int_tuple(self) -> tuple[int, int]:
        """Return the Vector as a tuple."""
        return int(self.x), int(self.y)

    def __eq__(self, other: object) -> bool:
        """Check equality (with float tolerance)."""
        if not isinstance(other, Vector2):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __add__(self, other: Vector2) -> Vector2:
        """Addition."""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        """Subtraction."""
        return Vector2(self.x - other.x, self.y - other.y)

    @overload
    def __mul__(self, other: float) -> Vector2: ...
    @overload
    def __mul__(self, other: Vector2) -> Vector2: ...

    def __mul__(self, other: float | Vector2) -> Vector2:
        """Multiply vector by scalar or component-wise by another vector."""
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    @overload
    def __rmul__(self, other: float) -> Vector2: ...
    @overload
    def __rmul__(self, other: Vector2) -> Vector2: ...

    def __rmul__(self, other: float | Vector2) -> Vector2:
        """Right-hand multiplication (scalar * vector or vector * vector)."""
        return self.__mul__(other)

    @overload
    def __truediv__(self, other: float) -> Vector2: ...
    @overload
    def __truediv__(self, other: Vector2) -> Vector2: ...

    def __truediv__(self, other: float | Vector2) -> Vector2:
        """Divide vector by scalar or component-wise by another vector."""
        if isinstance(other, Vector2):
            return Vector2(
                self.x / other.x if other.x != 0 else 0.0,
                self.y / other.y if other.y != 0 else 0.0,
            )
        return Vector2(self.x / other, self.y / other)

    @overload
    def __floordiv__(self, other: float) -> Vector2: ...
    @overload
    def __floordiv__(self, other: Vector2) -> Vector2: ...

    def __floordiv__(self, other: float | Vector2) -> Vector2:
        """Floor divide by scalar or component-wise by vector."""
        if isinstance(other, Vector2):
            return Vector2(
                self.x // other.x,
                self.y // other.y,
            )
        return Vector2(self.x // other, self.y // other)

    @overload
    def __ifloordiv__(self, other: float) -> Self: ...
    @overload
    def __ifloordiv__(self, other: Vector2) -> Self: ...

    def __ifloordiv__(self, other: float | Vector2) -> Self:
        """In-place floor division."""
        if isinstance(other, Vector2):
            self.x //= other.x
            self.y //= other.y
        else:
            self.x //= other
            self.y //= other
        return self

    def __neg__(self) -> Vector2:
        """Negation."""
        return Vector2(-self.x, -self.y)

    def __abs__(self) -> Vector2:
        """Absolute value."""
        return Vector2(abs(self.x), abs(self.y))

    def __iadd__(self, other: Vector2) -> Self:
        """In place addition multiplication."""
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Vector2) -> Self:
        """In place subtraction multiplication."""
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other: float | Vector2) -> Self:
        """In-place multiplication by scalar or component-wise by vector."""
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    @overload
    def __itruediv__(self, other: float) -> Self: ...
    @overload
    def __itruediv__(self, other: Vector2) -> Self: ...

    def __itruediv__(self, other: float | Vector2) -> Self:
        """In-place division by scalar or component-wise by vector."""
        if isinstance(other, Vector2):
            self.x = self.x / other.x if other.x != 0 else 0.0
            self.y = self.y / other.y if other.y != 0 else 0.0
        else:
            self.x /= other
            self.y /= other
        return self

    def magnitude(self) -> float:
        """Return vector length."""
        return math.hypot(self.x, self.y)

    def magnitude_squared(self) -> float:
        """Return squared length (avoids sqrt for performance)."""
        return self.x * self.x + self.y * self.y

    def normalize(self) -> Vector2:
        """Return normalized vector."""
        mag = self.magnitude()
        if mag == 0.0:
            return Vector2(0.0, 0.0)
        return self / mag

    def normalize_ip(self) -> None:
        """Normalize in place."""
        mag = self.magnitude()
        if mag != 0.0:
            self.x /= mag
            self.y /= mag

    def distance_to(self, other: Vector2) -> float:
        """Distance between two vectors."""
        return (self - other).magnitude()

    def distance_squared_to(self, other: Vector2) -> float:
        """Distance squared between vectors. Performance thing if you are just comparing distances."""
        return (self - other).magnitude_squared()

    def dot(self, other: Vector2) -> float:
        """2D dot product (x * x + y * y)."""
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector2) -> float:
        """2D cross product (scalar result)."""
        return self.x * other.y - self.y * other.x

    def angle(self) -> float:
        """Angle from origin in radians."""
        return math.atan2(self.y, self.x)

    def angle_to(self, other: Vector2) -> float:
        """Angle to another vector in radians."""
        return math.atan2(other.y - self.y, other.x - self.x)

    def rotate(self, radians: float) -> Vector2:
        """Return rotated vector."""
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)
        return Vector2(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta,
        )

    def rotate_ip(self, radians: float) -> None:
        """Rotate in place."""
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)
        x = self.x * cos_theta - self.y * sin_theta
        y = self.x * sin_theta + self.y * cos_theta
        self.x = x
        self.y = y

    def lerp(self, other: Vector2, t: float) -> Vector2:
        """Linear interpolation."""
        return Vector2(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
        )

    def project_onto(self, other: Vector2) -> Vector2:
        """Project this vector onto another."""
        denom = other.magnitude_squared()
        if denom == 0.0:
            return Vector2(0.0, 0.0)
        return other * (self.dot(other) / denom)

    def reflect(self, normal: Vector2) -> Vector2:
        """Reflect vector across a normal."""
        return self - 2 * self.dot(normal) * normal

    def clamp(self, min_v: Vector2, max_v: Vector2) -> Vector2:
        """Clamp vector between two vectors."""
        return Vector2(
            max(min_v.x, min(self.x, max_v.x)),
            max(min_v.y, min(self.y, max_v.y)),
        )

    @classmethod
    def zero(cls) -> Vector2:
        """Create a (0, 0) Vector."""
        return Vector2(0, 0)

    @classmethod
    def one(cls) -> Vector2:
        """Create a (1, 1) Vector."""
        return Vector2(1, 1)
