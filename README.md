# k8s-describe-nodes-parser

Some simple dumb python script to parse `kubectl describe nodes`,
tailored to parse nvidia gpu-feature-discovery output.
Returns output as JSON, for easier parsing.

tl;dr:
I had to do some simple detection if env will fit in k8s cluster with
nvidia gpus, so this is a small helper script.

The superpowers of bash comes when you mix it with `jq`:

```bash
$ python3 k8s_resources.py --input data/nodes-fake.txt | jq '[.[]|.gpu.requests]|add'
0
```

## Example

See [data/](data/) directory for input and output.

```bash
python3 k8s_resources.py --input data/nodes-fake.txt  > data/output.json
```

Example output (snippet):

```text
[
  {
    "name": "alpha",
    "cpu": {
      "requests": "925m",
      "requests_percent": 10,
      "limits": "3",
      "limits_percent": 33
    },
    "mem": {
      "requests": "1869366Ki",
      "requests_percent": 3,
      "limits": "6315402496",
      "limits_percent": 10
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    },
    "ephemeral-storage": {
      "requests": "0",
      "requests_percent": 0,
      "limits": "0",
      "limits_percent": 0
    },
    "hugepages-2Mi": {
      "requests": "0",
      "requests_percent": 0,
      "limits": "0",
      "limits_percent": 0
    },
    "hugepages-1Gi": null
  },
  {
    "name": "bravo",
    "cpu": {
      "requests": "725m",
      "requests_percent": 8,
      "limits": "2",
      "limits_percent": 22
    },
    "mem": {
      "requests": "1345078Ki",
      "requests_percent": 2,
      "limits": "5241660672",
      "limits_percent": 8
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    },
    "ephemeral-storage": {
      "requests": "0",
      "requests_percent": 0,
      "limits": "0",
      "limits_percent": 0
    },
    "hugepages-2Mi": {
      "requests": "0",
      "requests_percent": 0,
      "limits": "0",
      "limits_percent": 0
    },
    "hugepages-1Gi": null
  }
]
```

## References

* [jq](https://stedolan.github.io/jq/)
* [python3](https://pythonclock.org/)

## Contributing

Yeah you can try, but be prepared that they will be rejected.
