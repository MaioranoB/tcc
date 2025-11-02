import os
import re
import pandas as pd
from datetime import datetime
from argparse import Namespace
from constants import RESULTS_DIR

def create_result_dataframe(algorithms: list[str]) -> pd.DataFrame:
    fixed_cols = ["Graph", "|V|", "|E|"]
    algorithm_results_cols = ["|CBC|", "Time (s)"]

    df_tuples = [(col, '') for col in fixed_cols]

    for algorithm_name in algorithms:
        for result_col in algorithm_results_cols:
            df_tuples.append((algorithm_name, result_col))

    columns = pd.MultiIndex.from_tuples(df_tuples)
    return pd.DataFrame(columns=columns)

def get_graph_name(path: str) -> str:
    # '/path/to/benchmarks/brock200_1.clq' -> 'brock200_1'
    return os.path.splitext(os.path.basename(path))[0]

def get_base_dir(path: str) -> str:
    # '/path/to/benchmarks/' -> 'benchmarks'
    return os.path.basename(os.path.normpath(path))

def result_filename_from_args(args: Namespace) -> str:
    algorithm_str = "ALL" if args.ALL else args.algorithm
    
    file_str = get_graph_name(args.file) if args.file else get_base_dir(args.fileDir)
    if args.fileDir and args.family:
        file_str += f" {args.family}"
    
    timestamp = datetime.now().strftime("%d%m-%H%M")
    
    file_name =  f"{algorithm_str} {file_str} limit{args.time}s {timestamp}"

    if not os.path.exists(RESULTS_DIR): os.makedirs(RESULTS_DIR)
    return os.path.join(RESULTS_DIR, file_name)

def mixed_sort_key(file_path: str) -> list:
    file_name = get_graph_name(file_path)
    parts = re.split(r'(\d+)', file_name) # 'brock200_1' -> ['brock', '200', '_', '1']

    sort_key = []
    for part in parts:
        if part.isdigit():
            sort_key.append(int(part))
        else:
            sort_key.append(part)
    
    return sort_key

def get_graph_files_from_dir(dir: str, familyFilter = "") -> list:
    graph_files = []
    for file in os.listdir(dir):
        if familyFilter and not file.startswith(familyFilter): continue
        if file.endswith(".clq") or file.endswith(".txt"):
            graph_files.append(os.path.join(dir, file))
    
    graph_files.sort(key=mixed_sort_key)
    return graph_files