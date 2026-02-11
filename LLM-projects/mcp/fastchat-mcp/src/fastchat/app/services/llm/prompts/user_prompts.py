def service2args(query: str, service: dict):
    return "{" + f'"User Query": {query}, "Service":{service}' + "}"
    # return f'{query}.\n Use the following service as information base:\n{service}'


def query_and_services(query: str, services: str | list):
    return "{" + f'"User Query": {query}, "All Services":{services}' + "}"
    # return f"{query}.\n The available services for obtaining information are:\n{services}"


def exposed_prompts(prompt_services: str | list):
    return (
        f"All prompt services:{prompt_services}"
        if len(prompt_services) > 0
        else "There are not prompts aviables. Your respose should be `[]`."
    )


def query_and_data(query: str, data: str | dict):
    return f"{query}.\n Use the following retrievd data to answer my query:\n{data}"
    # return "{" + f'"User Query": {query}, "Context":{data}' + "}"
