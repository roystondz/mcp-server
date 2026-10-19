
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Query the MCP documentation assistant."
    )

    parser.add_argument(
        "--query",
        required=True,
        help="The question you want answered.",
    )

    parser.add_argument(
        "--library",
        required=True,
        help="Documentation library to search.",
    )

    return parser.parse_args()
