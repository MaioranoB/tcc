import os
import subprocess

# Usage: ./benchmark/DIMACS/binformat/bin2asc infile [outfile]

relpath = os.path.relpath("benchmark/DIMACS")

bin2asc = os.path.join(relpath, "binformat", "bin2asc")
infile_path = os.path.join(relpath, "binaries")

def main():
    for file in os.listdir(infile_path):
        infile = os.path.join(infile_path, file)

        outfile_name = os.path.splitext(file)[0]
        outfile = os.path.join(relpath, outfile_name)

        command = f'{bin2asc} {infile} {outfile}'.split()
        subprocess.run(command)
    return

if __name__ == "__main__":
    main()