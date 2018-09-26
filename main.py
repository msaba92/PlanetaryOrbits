import random
import matplotlib.pyplot as plot


class Body:
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    markers = ["^", "<", ">", "v"]

    def __init__(self, location, mass, velocity, is_fixed, color=None, marker=None):
        self.initial_location = location
        self.location = location
        self.mass = mass
        self.velocity = velocity

        self.historical_locations = {"x": [], "y": []}

        self.acceleration = PositionalClass(0, 0)
        self.is_fixed = is_fixed

        if not color:
            self.color = random.choice(self.colors)
        else:
            self.color = color

        if not marker:
            self.marker = random.choice(self.markers)
        else:
            self.marker = marker

    def r_cubic(self, target_body_x, target_body_y):
        r = (self.location.x - target_body_x) ** 2 \
          + (self.location.y - target_body_y) ** 2

        r = r ** .5

        return r ** 3


class PositionalClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def calculate_each_step(bodies, timestep):
    G = 6.67408e-11

    for body in bodies:
        acceleration = PositionalClass(0, 0)
        for external_body in bodies:
            if body != external_body:

                r_cubic = bodies[body].r_cubic(
                    bodies[external_body].location.x,
                    bodies[external_body].location.y
                    )

                acc = G * bodies[external_body].mass / r_cubic

                acceleration.x += acc * (bodies[external_body].location.x - bodies[body].location.x)
                acceleration.y += acc * (bodies[external_body].location.y - bodies[body].location.y)

        if not bodies[body].is_fixed:
            bodies[body].location.x += timestep * (
                bodies[body].velocity.x + timestep * acceleration.x / 2
                )
            bodies[body].location.y += timestep * (
                bodies[body].velocity.y + timestep * acceleration.y / 2
                )

            old_acceleration = acceleration
            acceleration = PositionalClass(0, 0)
            for external_body in bodies:
                if body != external_body:

                    r_cubic = bodies[body].r_cubic(
                        bodies[external_body].location.x,
                        bodies[external_body].location.y
                        )

                    acc = G * bodies[external_body].mass / r_cubic

                    acceleration.x += acc * (
                        bodies[external_body].location.x - bodies[body].location.x
                        )
                    acceleration.y += acc * (
                        bodies[external_body].location.y - bodies[body].location.y
                        )

            bodies[body].velocity.x += timestep * (acceleration.x + old_acceleration.x) / 2
            bodies[body].velocity.y += timestep * (acceleration.y + old_acceleration.y) / 2


def main(number_of_steps, bodies):
    fig = plot.figure()
    ax = fig.add_subplot(1, 1, 1)

    for i in range(1, number_of_steps):
        calculate_each_step(bodies, i)

        for body in bodies:
            bodies[body].historical_locations["x"].append(bodies[body].location.x)
            bodies[body].historical_locations["y"].append(bodies[body].location.y)

    max_range, min_range = (0, 0)
    for body in bodies:
        max_dim = max(
            max(bodies[body].historical_locations["x"]),
            max(bodies[body].historical_locations["y"])
            )
        min_dim = min(
            min(bodies[body].historical_locations["x"]),
            min(bodies[body].historical_locations["y"])
            )
        if max_dim > max_range:
            max_range = max_dim
        if min_dim < min_range:
            min_range = min_dim

        ax.plot(
            bodies[body].historical_locations["x"],
            bodies[body].historical_locations["y"],
            c=bodies[body].color,
            label=body
            )

    min_range = min(-max_range, min_range)

    ax.set_xlim([min_range*1.2, max_range*1.2])
    ax.set_ylim([min_range*1.2, max_range*1.2])

    for body, body_props in bodies.items():
        if body_props.is_fixed:
            plot.scatter(
                body_props.initial_location.x,
                body_props.initial_location.y,
                c=body_props.color,
                marker=body_props.marker
                )
        else:
            plot.scatter(
                body_props.location.x,
                body_props.location.y,
                c=body_props.color,
                marker=body_props.marker
                )

    plot.legend()
    plot.show()


def point_a():
    global au
    global tau

    years = 10
    number_of_steps = int(years / tau)

    bodies = {
        "first star": Body(
            location=PositionalClass(-3*au, 0),
            mass=1.989e30,
            velocity=PositionalClass(0, 0),
            is_fixed=True,
            color="b",
            marker="^"
            ),
        "second star": Body(
            location=PositionalClass(3*au, 0),
            mass=1.989e30,
            velocity=PositionalClass(0, 0),
            is_fixed=True,
            color="y",
            marker="^"
            ),

        "first planet": Body(
            location=PositionalClass(0, au*5),
            mass=4.8e24,
            velocity=PositionalClass(2e4, 0),
            is_fixed=False,
            color="r",
            marker="o"
            ),
        }

    main(number_of_steps, bodies)


def point_b():
    global au
    global tau

    years = 2
    number_of_steps = int(years / tau)

    bodies = {
        "first star": Body(
            location=PositionalClass(0, 0),
            mass=1.989e30,
            velocity=PositionalClass(0, 0),
            is_fixed=True,
            color="b",
            marker="^"
            ),

        "first planet": Body(
            location=PositionalClass(0, au*1.41),
            mass=4.8e24,
            velocity=PositionalClass(1.3e4, 0),
            is_fixed=False,
            color="r",
            marker="o"
            ),

        "second planet": Body(
            location=PositionalClass(0, au*1.40),
            mass=4.8e25,
            velocity=PositionalClass(1.3e4, 0),
            is_fixed=False,
            color="y"
            ),
        }

    main(number_of_steps, bodies)


if __name__ == "__main__":
    au = 1.5e11
    tau = .0001

    point_a()
    point_b()
