import sys
import pandas as pd
from Graph import read_dimacs_graph
from CurrentBestClique import CBC
from algorithms import ALGORITHMS
from utils import timing, result, arguments

def run_algorithm(algorithm_name: str, time_limit: int):
    algorithm = ALGORITHMS[algorithm_name]
    max_clique = 0
    time = ""

    try:
        with timing.time_limit(time_limit):
            _, elapsed_time = timing.measure_algorithm_runtime(algorithm)
            max_clique = CBC()
            time = f"{elapsed_time:.3f}"
            print(f"{algorithm_name.ljust(7)} - CBC  = {max_clique} - Elapsed time = {time} seconds")
    except timing.TimeoutException:
        max_clique = f">= {CBC()}"
        time = "-"
        print(f"{algorithm_name.ljust(7)} - CBC {max_clique} - TIMED OUT!")
    except RecursionError:
        max_clique = f">= {CBC()}"
        time = "recursion depth exceeded"
        print(f"{algorithm_name.ljust(7)} - CBC {max_clique} - MAXIMUM RECURSION DEPTH ({sys.getrecursionlimit()}) EXCEEDED!")
    except KeyboardInterrupt:
        max_clique = f">= {CBC()}"
        time = "keyboard interrupt"
        print(f"{algorithm_name.ljust(7)} - CBC {max_clique} - KEYBOARD INTERRUPTED!")

    return max_clique, time

def confirm_execution(graphCount: int, algorithmsCount: int, time: int) -> bool:
    def plurarize(word: str, count: int):
        return word if count == 1 else word + "s"
    
    alg_word = plurarize("algorithm", algorithmsCount)
    graph_word = plurarize("graph", graphCount)
    second_word = plurarize("second", time)
    print(f"{algorithmsCount} {alg_word} to be executed on {graphCount} {graph_word} with a time limit of {time} {second_word} each.")

    total_executions = graphCount * algorithmsCount
    print(f"Total of {total_executions} algorithm executions. Possible duration time: ~{(total_executions * time) / 3600:.2f} hours.")

    response = input("\nDo you want to proceed? (y/n): ").strip().lower()
    if response != 'y': return False
    return True

def main():
    args = arguments.parse_command_line()

    graph_files = [args.file] if args.file else result.get_graph_files_from_dir(args.fileDir, args.family)
    algorithms = ALGORITHMS.keys() if args.ALL else [args.algorithm]
    time_limit = args.time

    if not confirm_execution(len(graph_files), len(algorithms), time_limit):
        return

    sys.setrecursionlimit(1500) # default 1000
    
    df = result.create_result_dataframe(algorithms)
    
    for graph_file in graph_files:
        graph_name = result.get_graph_name(graph_file)
        G, read_graph_time = timing.measure_algorithm_runtime(read_dimacs_graph, graph_file)

        print(f"-------- {read_graph_time:.5f} seconds to read {graph_name} --------")

        algorithm_results = []
        for algorithm_name in algorithms:
            max_clique, elapsed_time = run_algorithm(algorithm_name, time_limit)
            algorithm_results.extend([max_clique, elapsed_time])

        nodes = G.number_of_nodes()
        edges = G.number_of_edges()

        df.loc[len(df)] = [graph_name, nodes, edges] + algorithm_results
        print()

    filename = result.result_filename_from_args(args)
    # df.to_csv(f"{filename}.csv", index=False)
    df.to_excel(f"{filename}.xlsx")
    return

if __name__ == "__main__":
    main()
