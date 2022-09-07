

from email.generator import Generator
from fileinput import filename

filename = 'log.txt'



def _get_date(line: str) -> str:
    return line.split(' ')[0]

def _get_level(line: str) -> str:
    LEVELS = ['INFO', 'ERROR', 'WARNING', 'TRACE']
    for level in LEVELS:
        if level in line:
            return level
    return 'UNDEFIEND'

def _mapper(line: str) -> tuple[str, int]:
    date = _get_date(line)
    level = _get_level(line)
    return (date, level), 1

def _reducer(key: str, values: list[int]) -> tuple[str, int]:
    return sum(values)

def _read_file(filename: str) -> Generator:
    with open(filename, "rt") as f:
        for line in f:
            yield line

def log_parser(filename: str) -> None:
    mapped = [_mapper(line) for line in _read_file(filename)]
    results = {}
    for key, value in mapped:
        results[key] = _reducer(key, [results.get(key, 0), value])
    return results



if __name__ == '__main__':
    for key, value in log_parser(filename).items():
        print(key, value)
