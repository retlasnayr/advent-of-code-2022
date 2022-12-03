def read_in_file(file_path):
    """
    Read in text file at file path, then split to a list on the newline (\n) character
    :param file_path: Local file path to read in
    :return: List of strings, each element is one line from the input file.
    """
    with open(file_path) as f:
        input_lines = f.read()
        input_lines = input_lines.split("\n")
    return input_lines
