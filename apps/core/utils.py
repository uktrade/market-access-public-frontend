def convert_to_snake_case(value):
    value = value.lower().replace(" ", "_").replace("-", "_")
    return ''.join([i for i in value if i.isalpha() or i == "_"])


def chain(*iterables):
    for iterable in iterables:
        yield from iterable
