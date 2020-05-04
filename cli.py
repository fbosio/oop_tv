import argparse


def options():
    """Get dict with app options parsed from command line."""
    DEFAULT_NAME = 'my_television_instance'

    parser = argparse.ArgumentParser(description='A little PyQt5 app to teach '
                                     'how instances work in Object Oriented '
                                     'Programming. ')
    parser.add_argument('-g', '--geometry', type=float,
                        nargs=4, metavar=('X', 'Y', 'WIDTH', 'HEIGHT'),
                        help='position of the window on screen')
    parser.add_argument('-n', '--name', default=DEFAULT_NAME,
                        help='name of your Television object instance.\n'
                        'This name is placed as the window title of the app '
                        f'(default: {DEFAULT_NAME}).')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="show what's going on behind the scenes")
    args = parser.parse_args()

    _options = {'debug': args.verbose, 'geometry': args.geometry,
                'title': args.name}

    return _options
