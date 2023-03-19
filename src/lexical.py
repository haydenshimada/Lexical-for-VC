import argparse
import json
import time

import hydra 
from omegaconf import DictConfig

from function import *

@hydra.main(version_base=None, config_path='../config', config_name='file')
def main(cfg: DictConfig):
    filename = cfg.file_name
    datafile = cfg.data_file
    no_comments = cfg.no_comments

    # Read the source code and data file containing the DFA
    source = read_file(filename)
    with open(datafile, "r") as file:
        data = json.load(file)
        KEYWORDS = data["keywords"]
        SPECIAL_LITERALS = data["special_literals"]
        SEPARATORS = data["separators"]
        TOKEN_TYPES = data["terminal_types"]
        nodes = data["nodes"]

    # Parse the source code
    print("Parsing file: " + filename)
    start = time.time()
    result = lexer(source, nodes, KEYWORDS, SPECIAL_LITERALS, SEPARATORS)
    end = time.time()
    print(f"Done in {end-start:.3f} seconds.")

    # Remove comments if the user specified the -n or --no-comments option
    if no_comments:
        result = [token for token in result if token["type"] != "COMMENT"]

    # Export the tokens
    verbose = "======= The VC compiler ======="
    for token in result:
        verbose += f"\nKind = {TOKEN_TYPES.index(token['type'])} [{token['type']}]"
        verbose += f", spelling = \"{token['token']}\""
        verbose += f", position = {token['line']}({token['start']})..{token['line']}({token['end']})"

    output = ""
    for token in result:
        output += token["token"]
        output += "\n"

    verbose_filename = filename.split(".")[0] + ".verbose.vctok"
    with open(verbose_filename, "w+") as file:
        file.write(verbose)

    output_filename = filename.split(".")[0] + ".vctok"
    with open(output_filename, "w+") as file:
        file.write(output)

    print("Exported tokens to: " + output_filename)
    print("Exported verbose tokens to: " + verbose_filename)


if __name__ == "__main__":
    main()    
