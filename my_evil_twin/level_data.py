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
        None, # Color separator
        {
            'type': 'floor',
            'pos1': (-100, -100),
            'pos2': (100, 100)
        },
        ## END MAIN AREA

        ## P1 AREA
        {
            'type': 'wall_z',
            'x_min': -20,
            'x_max': 5,
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
            'x': 5,
            'direction': 1
        },
        {
            'type': 'wall_z',
            'x_min': 5,
            'x_max': 20,
            'y_min': 0,
            'y_max': 5,
            'z': -35,
            'direction': 1
        },
        ## END P1 AREA

        ## P2 AREA
        {
            'type': 'wall_z',
            'x_min': -20,
            'x_max': 20,
            'y_min': 0,
            'y_max': 5,
            'z': 20,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -20,
            'z_max': 20,
            'y_min': 0,
            'y_max': 5,
            'x': -20,
            'direction': 1
        },
        ## END P2 AREA

        {
            'type': 'deep_line_x',
            'x_min': -10,
            'x_max': -5,
            'z_min': -2,
            'z_max': 2,
            'equation': '-x - 5'
        }
    ]
})
