"""Parse 'kubectl describe nodes', convert to json.

see --help

tl;dr we need to get some easy output of nodes and number of used gpus
and then we do some super hardore science with it like
"if number of gpu used is over 4 then fail creating k8s 'env with gpu'"

"""

import argparse
import json
import sys
import re


def parse_percent(input_str):
    """parse '(number%)' to 'number' as int
    """
    result = re.search(r"\(([0-9]+)%\)", input_str)
    return int(result.group(1))


def get_name(line):
    """get node name

    Yeah, This Is Big Brain Time
    """
    line = line.split(":")
    node_name = line[1].strip()
    return node_name


def get_cpu(line):
    """get cpu requests/limits
    """
    line = line.split()
    cpu = {
        'requests': line[1],
        'requests_percent': parse_percent(line[2]),
        'limits': line[3],
        'limits_percent': parse_percent(line[4]),
    }
    return cpu


def get_memory(line):
    """get memory requests/limits
    """
    line = line.split()
    mem = {
        'requests': line[1],
        'requests_percent': parse_percent(line[2]),
        'limits': line[3],
        'limits_percent': parse_percent(line[4]),
    }
    return mem


def get_nvidia(line):
    """get nvidia requests/limits
    ensure to have installed nvidia gpu-feature-discovery in the k8s cluster
    """
    line = line.split()
    gpu = {
        'requests': int(line[1]),
        'limits': int(line[2]),
    }
    return gpu


def get_ephemeral(line):
    """get ephemeral storage
    """
    line = line.split()
    eph = {
        'requests': line[1],
        'requests_percent': parse_percent(line[2]),
        'limits': line[3],
        'limits_percent': parse_percent(line[4]),
    }
    return eph


def get_hugepages(line):
    """get hugepages
    """
    line = line.split()
    eph = {
        'requests': line[1],
        'requests_percent': parse_percent(line[2]),
        'limits': line[3],
        'limits_percent': parse_percent(line[4]),
    }
    return eph


def get_allocated(lines):
    """get resource allocation on the node
    """
    line = lines.__next__()
    cpu = None
    mem = None
    gpu = None
    eph = None
    huge_2Mi = None
    huge_1Gi = None

    # lines is a interator over an output, we seek for specific
    # output section, usually anything below 'Events' can be dropped
    while not line.startswith("Events"):

        # todo, do some more nice processing to allow dynamic creation of data
        line = line.strip()
        if line.startswith('cpu'):
            cpu = get_cpu(line)
        elif line.startswith('memory'):
            mem = get_memory(line)
        elif line.startswith('nvidia.com/gpu'):
            gpu = get_nvidia(line)
        elif line.startswith('ephemeral-storage'):
            eph = get_ephemeral(line)
        elif line.startswith('hugepages-2Mi'):
            huge_2Mi = get_hugepages(line)
        elif line.startswith('hugepages-1Gi'):
            huge_1Gi = get_hugepages(line)

        line = lines.__next__()

    result = {
        'cpu': cpu,
        'mem': mem,
        'gpu': gpu,
        'ephemeral-storage': eph,
        'hugepages-2Mi': huge_2Mi,
        'hugepages-1Gi': huge_1Gi
    }
    return result


def parse(lines):
    """parse lines(list) and extract data about node
    """
    nodes = []
    if lines.__sizeof__() > 0:
        for line in lines:
            # extract node name
            if line.startswith("Name"):
                node = {}
                node['name'] = get_name(line)
            # extract allocated resources
            elif line.startswith('Allocated resources'):
                data = get_allocated(lines)
                for k, v in data.items():
                    node[k] = v
                nodes.append(node)
    return nodes


def pretty(data):
    """pretty print given data
    """
    return json.dumps(data, indent=2)


def run():
    """
    Parses arguments and runs the script
    """
    epilog = """
    Example usage:

    Use stdin and stdout:
        kubectl describe nodes | python3 k8s_resources.py | jq '[.[]|.gpu.requests]|add'

    Use specific files for input and output:
        kubectl describe nodes > output.txt
        python3 k8s_resources.py -i output.txt

    """
    parser = argparse.ArgumentParser(
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-i", "--input",
        help='input, can be from stdin or file, this should be output of kubectl describe nodes',
        type=argparse.FileType('r'),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help='Where to pass parsed output, default stdout',
        type=argparse.FileType('w'),
        default=sys.stdout,
    )
    args = parser.parse_args()

    data = args.input
    output = args.output

    data_list = parse(data)
    pretty_json = pretty(data_list)
    output.write(pretty_json)


if __name__ == '__main__':
    run()
