import os

def trim_and_add_hyphens(string):
    trimmed_string = string.strip()
    split_string = trimmed_string.split()
    modified_string = "-".join(split_string)
    return modified_string

def input_output_folder():
    return f"{os.path.dirname(os.path.abspath(__file__))}/spiders/output"

