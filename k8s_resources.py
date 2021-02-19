"""
Parse 'kubectl describe nodes', convert to json that you may not like.
tl;dr we need to get some easy output of nodes and number of used gpus
and then we do some super hardore science with it like
"if number of gpu used is over 4 then fail creating k8s 'env with gpu'"

hyper bash science below:

    python3 k8s_resources.py | jq '[.[]|.gpu.requests]|add'

"""

import io
import json
import re
import subprocess


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


def get_allocated(lines):
    """get resource allocation on the node
    """
    line = lines.__next__()
    cpu = None
    mem = None
    gpu = None

    # lines is a interator over an output, we seek for specific
    # output section, usually anything below 'Events' can be dropped
    while not line.startswith("Events"):

        if line.strip().startswith('cpu'):
            cpu = get_cpu(line)
        elif line.strip().startswith('memory'):
            mem = get_memory(line)
        elif line.strip().startswith('nvidia'):
            gpu = get_nvidia(line)

        line = lines.__next__()

    return {'cpu': cpu, 'mem': mem, 'gpu': gpu}


def kubectl_describe_nodes():
    """run kubectl process and grab its output

    process only instances with nvidia gpu labels
    """
    command = 'kubectl describe nodes -l nvidia.com/gpu.count'
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    return io.TextIOWrapper(process.stdout, encoding="utf-8")


def parse(lines):
    """parse lines(list) and extract data about node
    """
    nodes = []
    if lines.__sizeof__() > 0:
        for line in lines:
            if line.startswith("Name"):
                node = {}
                node['name'] = get_name(line)

            elif line.startswith('Allocated resources'):
                # todo: make it less dumb copy-paste in the future (aka never)
                data = get_allocated(lines)
                node['mem'] = data['mem']
                node['cpu'] = data['cpu']
                node['gpu'] = data['gpu']
                nodes.append(node)
    return nodes


def pretty(data):
    """pretty print given data
    """
    return json.dumps(data, indent=2)


def get():
    """get output from kubectl, parse and output into some nightmare format
    """
    output = kubectl_describe_nodes()
    nodes = parse(output)
    return nodes


if __name__ == '__main__':
    print(pretty(get()))
