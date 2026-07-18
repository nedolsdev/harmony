"""CollisionResolver resolves some physics based collisions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.components.transform import Transform
from harmony.core.packages.geometry.vector2 import Vector2

if TYPE_CHECKING:
    from harmony.core.packages.collision.rigidbody_collision import CollisionRigidBody2D


class CollisionResolver:
    """CollisionResolver resolves physics based collisions."""

    POSITION_SLOP: float = 0.01
    POSITION_CORRECTION: float = 0.8

    EPSILON = 1e-8

    @staticmethod
    def solve_collision(collision: CollisionRigidBody2D) -> None:
        """Solve a Collision between two RigidBody2D."""
        a = collision.rigid_body_a
        b = collision.rigid_body_b
        contact = collision.contact

        a_transform = a.game_object.get_component(Transform)
        b_transform = b.game_object.get_component(Transform)

        normal: Vector2 = contact.normal
        restitution: float = contact.restitution

        for contact_point in contact.contact_points:
            ra: Vector2 = contact_point - (a_transform.world_position + a.center_of_mass)
            rb: Vector2 = contact_point - (b_transform.world_position + b.center_of_mass)

            # relative velocity at contact
            rv: Vector2 = (
                b.velocity
                + Vector2(-b.angular_velocity * rb.y, b.angular_velocity * rb.x)
                - a.velocity
                - Vector2(-a.angular_velocity * ra.y, a.angular_velocity * ra.x)
            )

            vel_along_normal: float = rv.dot(normal)

            # do not resolve if separating
            if vel_along_normal > 0:
                continue

            ra_cross_n: float = ra.x * normal.y - ra.y * normal.x
            rb_cross_n: float = rb.x * normal.y - rb.y * normal.x

            inv_mass_sum: float = (
                a.inverse_mass
                + b.inverse_mass
                + (ra_cross_n * ra_cross_n) * a.inverse_inertia
                + (rb_cross_n * rb_cross_n) * b.inverse_inertia
            )

            if inv_mass_sum == 0:
                continue

            # normal impulse
            j: float = -(1 + restitution) * vel_along_normal
            j /= inv_mass_sum
            j /= len(contact.contact_points)

            impulse: Vector2 = normal * j

            a.velocity -= impulse * a.inverse_mass
            b.velocity += impulse * b.inverse_mass

            a.angular_velocity -= ra.cross(impulse) * a.inverse_inertia
            b.angular_velocity += rb.cross(impulse) * b.inverse_inertia

            # friction
            rv = (
                b.velocity
                + Vector2(-b.angular_velocity * rb.y, b.angular_velocity * rb.x)
                - a.velocity
                - Vector2(-a.angular_velocity * ra.y, a.angular_velocity * ra.x)
            )

            tangent: Vector2 = rv - normal * rv.dot(normal)

            if tangent.magnitude_squared() > CollisionResolver.EPSILON:
                tangent = tangent.normalize()

                jt: float = -rv.dot(tangent)
                jt /= inv_mass_sum
                jt /= len(contact.contact_points)

                static_friction = contact.static_friction
                dynamic_friction = contact.dynamic_friction

                friction_impulse: Vector2

                friction_impulse = tangent * jt if abs(jt) < j * static_friction else tangent * -j * dynamic_friction

                a.velocity -= friction_impulse * a.inverse_mass
                b.velocity += friction_impulse * b.inverse_mass

                a.angular_velocity -= ra.cross(friction_impulse) * a.inverse_inertia
                b.angular_velocity += rb.cross(friction_impulse) * b.inverse_inertia

    @staticmethod
    def correct_positions(collision: CollisionRigidBody2D) -> None:
        """Correct positional penetration."""
        a = collision.rigid_body_a
        b = collision.rigid_body_b
        contact = collision.contact

        normal: Vector2 = contact.normal
        penetration: float = contact.penetration

        if penetration <= CollisionResolver.POSITION_SLOP:
            return

        correction_magnitude: float = (
            max(penetration - CollisionResolver.POSITION_SLOP, 0.0) / (a.inverse_mass + b.inverse_mass)
        ) * CollisionResolver.POSITION_CORRECTION

        correction: Vector2 = normal * correction_magnitude

        # push objects apart
        a_transform = a.game_object.get_component(Transform)
        b_transform = b.game_object.get_component(Transform)

        a_pos = a_transform.world_position
        b_pos = b_transform.world_position

        a_transform.world_position = a_pos - correction * a.inverse_mass
        b_transform.world_position = b_pos + correction * b.inverse_mass
