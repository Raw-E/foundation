import argparse

def parse_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.

    Raises:
        argparse.ArgumentError: If the provided arguments are invalid.
    """
    parser = argparse.ArgumentParser(description="Create a new Python package or a Python backend.")
    parser.add_argument("package_name", type=str, nargs='?', default=None, 
                        help="The name of the new package. Use quotes if the name contains spaces. Optional when creating a backend.")
    parser.add_argument("--backend", action="store_true", help="Create a Python backend instead of a package.")

    return parser.parse_args()