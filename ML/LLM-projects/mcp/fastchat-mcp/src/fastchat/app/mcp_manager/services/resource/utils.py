def get_args_from_uri(uri: str) -> list[str]:
    result = []
    current_arg = ""
    for char in uri:
        if char == "{":
            current_arg = ""
        elif char == "}":
            result.append(current_arg)
        else:
            current_arg += char
            
    return result
