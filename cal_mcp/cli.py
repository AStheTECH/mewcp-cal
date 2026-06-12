import argparse


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--transport",
        default=None
    )

    parser.add_argument(
        "--host",
        default=None
    )

    parser.add_argument(
        "--port",
        type=int,
        default=None
    )

    return parser.parse_args()