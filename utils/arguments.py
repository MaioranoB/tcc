import argparse
from constants import DEFAULT_TIME_LIMIT
from algorithms import ALGORITHMS

def parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="B&B algorithms for the exact solution of the maximum clique problem")
    parser.add_argument("-time", type=int, default=DEFAULT_TIME_LIMIT, help=f"time limit in seconds per algorithm. Default: {DEFAULT_TIME_LIMIT}s")

    file_group = parser.add_argument_group("Graph files (choose one)")
    
    file_group_exclusive = file_group.add_mutually_exclusive_group(required=True)
    file_group_exclusive.add_argument("-file", type=str, help="path to single DIMACS graph file")
    file_group_exclusive.add_argument("-fileDir", type=str, help="directory containing multiple DIMACS graph files")
    file_group.add_argument("-family", type=str, help="filter graphs by family name when using -fileDir (e.g., 'brock', 'c-fat', 'hamming')")

    algorithm_group = parser.add_argument_group("Algorithm selection (choose one)").add_mutually_exclusive_group(required=True)
    algorithm_group.add_argument("-algorithm", type=str, help="algorithm to use", choices=ALGORITHMS.keys())
    algorithm_group.add_argument("-ALL", action="store_true", help="run all algorithms")

    args = parser.parse_args()
    
    if args.time <= 0:
        parser.error("Time limit must be a positive integer.")

    # TODO: validate file/dir existence
    return args
