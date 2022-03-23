"""Am using a Python file to store the levels because
error checking."""

from my_evil_twin.level import Level

TEST_LEVEL = Level.parse({
    'elements': [
        {
            'type': 'sphere',
            'center': (4.5, 1.9, 3),
            'radius': 2
        },
        {
            'type': 'rectangle',
            'pos1': (0, 0, 0),
            'pos2': (2, 1, 4)
        },
        {
            'type': 'floor',
            'pos1': (-10, -10),
            'pos2': (10, 10)
        },
        {
            'type': 'wall_z',
            'x_min': -10,
            'x_max': 10,
            'y_min': 0,
            'y_max': 5,
            'z': 10,
            'direction': -1
        },
        {
            'type': 'wall_z',
            'x_min': -10,
            'x_max': 10,
            'y_min': 0,
            'y_max': 5,
            'z': -10,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': -10,
            'z_max': 10,
            'y_min': 0,
            'y_max': 5,
            'x': 10,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -10,
            'z_max': 10,
            'y_min': 0,
            'y_max': 5,
            'x': -10,
            'direction': 1
        },
        {
            'type': 'deep_line_x',
            'x_min': -10,
            'x_max': -5,
            'z_min': -2,
            'z_max': 2,
            'equation': '-x - 5'
        },
        {
            'type': 'deep_line_z',
            'x_min': -2,
            'x_max': 2,
            'z_min': -10,
            'z_max': -5,
            'equation': '-x - 5'
        }
    ]
})


LEVEL = Level.parse({
    'elements': [
        ## MAIN AREA
        {
            'type': 'floor',
            'pos1': (-20, -35),
            'pos2': (20, 35)
        },
        ## END MAIN AREA

        ## P1 AREA
        # Ground stuff
        {
            'type': 'wall_z',
            'x_min': -20,
            'x_max': 10,
            'y_min': 0,
            'y_max': 5,
            'z': -20,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': -35,
            'z_max': 20,
            'y_min': 0,
            'y_max': 5,
            'x': 20,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -35,
            'z_max': -20,
            'y_min': 0,
            'y_max': 5,
            'x': 10,
            'direction': 1
        },
        {
            'type': 'wall_z',
            'x_min': 10,
            'x_max': 20,
            'y_min': 0,
            'y_max': 5,
            'z': -35,
            'direction': 1
        },
        {
            'type': 'deep_line_z',
            'x_min': 16,
            'x_max': 20,
            'z_min': -35,
            'z_max': -30,
            'equation': '-x - 30'
        },
        # Second floor ground
        {
            'type': 'floor',
            'pos1': (10, -39),
            'pos2': (20, -35),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (20, -39),
            'pos2': (24, 24),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (6, -39),
            'pos2': (10, -20),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (-20, -24),
            'pos2': (6, -20),
            'y': 5
        },
        # Second floor walls
        {
            'type': 'wall_z',
            'x_min': 6,
            'x_max': 24,
            'y_min': 5,
            'y_max': 10,
            'z': -39,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': -39,
            'z_max': 24,
            'y_min': 5,
            'y_max': 10,
            'x': 24,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -39,
            'z_max': -24,
            'y_min': 5,
            'y_max': 10,
            'x': 6,
            'direction': 1
        },
        {
            'type': 'wall_z',
            'x_min': -24,
            'x_max': 6,
            'y_min': 5,
            'y_max': 10,
            'z': -24,
            'direction': 1
        },
        ## END P1 AREA

        ## P2 AREA
        # Ground stuff
        {
            'type': 'wall_z',
            'x_min': -10,
            'x_max': 20,
            'y_min': 0,
            'y_max': 5,
            'z': 20,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -20,
            'z_max': 35,
            'y_min': 0,
            'y_max': 5,
            'x': -20,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': 20,
            'z_max': 35,
            'y_min': 0,
            'y_max': 5,
            'x': -10,
            'direction': -1
        },
        {
            'type': 'wall_z',
            'x_min': -20,
            'x_max': -10,
            'y_min': 0,
            'y_max': 5,
            'z': 35,
            'direction': -1
        },
        {
            'type': 'deep_line_z',
            'x_min': -20,
            'x_max': -16,
            'z_min': 30,
            'z_max': 35,
            'equation': 'x - 30'
        },
        # Second floor ground
        {
            'type': 'floor',
            'pos1': (-20, 35),
            'pos2': (-10, 39),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (-24, -24),
            'pos2': (-20, 39),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (-10, 20),
            'pos2': (-6, 39),
            'y': 5
        },
        {
            'type': 'floor',
            'pos1': (-6, 20),
            'pos2': (20, 24),
            'y': 5
        },
        # Second floor walls
        {
            'type': 'wall_z',
            'x_min': -24,
            'x_max': -6,
            'y_min': 5,
            'y_max': 10,
            'z': 39,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -24,
            'z_max': 39,
            'y_min': 5,
            'y_max': 10,
            'x': -24,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': 24,
            'z_max': 39,
            'y_min': 5,
            'y_max': 10,
            'x': -6,
            'direction': -1
        },
        {
            'type': 'wall_z',
            'x_min': -6,
            'x_max': 24,
            'y_min': 5,
            'y_max': 10,
            'z': 24,
            'direction': -1
        },
        ## END P2 AREA

        ## RANDOM OBSTICLES
        # P1
        {
            'type': 'rectangle',
            'pos1': (-15, 0, -12),
            'pos2': (-10, 3.5, -10)
        },
        {
            'type': 'rectangle',
            'pos1': (-5, 0, -17),
            'pos2': (-3, 2.5, -14)
        },
        {
            'type': 'rectangle',
            'pos1': (5, 0, -9),
            'pos2': (9, 2, -4)
        },
        # P2
        {
            'type': 'rectangle',
            'pos1': (10, 0, 10),
            'pos2': (15, 3.5, 12)
        },
        {
            'type': 'rectangle',
            'pos1': (3, 0, 14),
            'pos2': (5, 2.5, 17)
        },
        {
            'type': 'rectangle',
            'pos1': (-9, 0, 4),
            'pos2': (-5, 2, 9)
        },
        ## END RANDOM OBSTICLES

        # {
        #     'type': 'deep_line_x',
        #     'x_min': -22,
        #     'x_max': -5,
        #     'z_min': -2,
        #     'z_max': 2,
        #     'equation': '-2.2 * x - 11'
        # }
    ]
})
