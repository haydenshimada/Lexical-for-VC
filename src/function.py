from hydra import compose, initialize

with initialize(config_path='../config', version_base=None):
    cfg = compose(config_name='const')
WHITESPACES = cfg.whitespaces
NEWLINE = cfg.newline
EXCLUDE = cfg.exclude

def read_file(path: str) -> str:
    """
    Args:
        path (str): path to the source code file

    Returns:
        str: a list of characters 
    """

    with open(path, "r") as file:
        return file.read()

def check_match(match: str, char: str) -> bool:
    """
    Args:
        match (str): a string of characters to match
        char (str): the character to check

    Returns:
        bool: True if the match contains the character, False otherwise
    """

    if match.startswith(EXCLUDE):
        return char not in match[len(EXCLUDE):]
    return char in match


def lexer(source: str, nodes: dict, keywords: list, boolean_literal: list, separators: str) -> list:
    """
    Args:
        source (str): the source code to parse
        nodes (dict): the nodes in the DFA
        keywords (list): the list of keywords
        special_literals (list): the list of special literals
        separators (str): the list of separators

    Returns:
        list: a list of tokens
    """

    # Initialize the starting state
    STARTING_STATE = "0"
    for id in nodes:
        if nodes[id]["starting"]:
            STARTING_STATE = id
            break

    tokens = []
    token = ""
    state = STARTING_STATE
    line = 1
    new_line_stack = ""
    position = 0
    start = position
    index = 0

    while index < len(source):
        char = source[index]
        index += 1
        position += 1
        
        # Skip whitespaces if the state is the starting state
        if state == STARTING_STATE and char in WHITESPACES:
            if char not in NEWLINE:
                new_line_stack = ""
            else:
                new_line_stack += char
                line += 1
                position = 0
            if new_line_stack.endswith(NEWLINE):
                new_line_stack = ""
                line -= 1
            continue
        
        # Check if current character matches any of the children
        children = nodes[state]["children"]
        found = False
        for match in children.keys():
            if check_match(match, char):
                state = children[match]
                if len(token) == 0:
                    start = position
                token += char
                found = True
                break
        
        # If no match is found, check if the current state is a terminal state
        if not found:
            index -= 1
            position -= 1

            # If the current state is a terminal state, add the token to the list of tokens
            if nodes[state]["terminal"] and (char in separators or token[-1] in separators):
                if token in keywords:
                    tokens.append({"token": token, "type": "Keyword", "line": line, "start": start, "end": position})
                elif token in boolean_literal:
                    tokens.append({"token": token, "type": "Boolean Literal", "line": line, "start": start, "end": position})
                else:
                    tokens.append({"token": token, "type": nodes[state]["terminal_type"], "line": line, "start": start, "end": position})
                if token.endswith("\n"):
                    line += 1
                    position = 0
                token = ""
                state = STARTING_STATE

            # If the current state is not a terminal state, print an error message
            else:
                error_msg = f"Error while parsing '{token}': invalid character at line {line}({position}): '{char}', "
                expecting = list(nodes[state]['children'].keys())
                for i in range(len(expecting)):
                    if expecting[i].startswith(EXCLUDE):
                        expecting[i] = "everything except '" + expecting[i][len(EXCLUDE):] + "'"
                    elif len(expecting[i]) == 1:
                        expecting[i] = "'" + expecting[i] + "'"
                    else:
                        expecting[i] = "one of {'" + "', '".join(expecting[i]) + "'}"
                expecting = sorted(expecting, key=lambda x: x.startswith("everything except"))
                error_msg += f"expected: {' or '.join(expecting)}"
                error_msg = error_msg.encode("unicode_escape").decode("utf-8")
                error_msg = error_msg.replace("\\\\", "\\")
                print(error_msg)
                token = ""
                state = STARTING_STATE

    # Add the last token to the list of tokens
    if token:
        if nodes[state]["terminal"]:
            if token in keywords:
                tokens.append({"token": token, "type": "Keyword", "line": line, "start": start, "end": position})
            elif token in boolean_literal:
                tokens.append({"token": token, "type": "Boolean Literal", "line": line, "start": start, "end": position})
            else:
                tokens.append({"token": token, "type": nodes[state]["terminal_type"], "line": line, "start": start, "end": position})

    return tokens
