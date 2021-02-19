# k8s-describe-nodes-parser

Some simple dumb python script to parse `kubectl describe nodes`,
tailored to parse nvidia gpu-feature-discovery output.

tl;dr:
I had to do some simpele detection if env will fit in k8s cluster with
nvidia gpus, so this is a small helper script.

Returns output as JSON, for easier parising.

The superpowers of bash comes when you mix it whith `jq`:

```bash
python3 k8s_resources.py | jq '[.[]|.gpu.requests]|add'
```

```bash
python k8s_resources.py 
```

```text
[
  {
    "name": "alpha",
    "mem": {
      "requests": "6063670Ki",
      "requests_percent": 9,
      "limits": "10610369792",
      "limits_percent": 16
    },
    "cpu": {
      "requests": "1225m",
      "requests_percent": 13,
      "limits": "5",
      "limits_percent": 56
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "bravo",
    "mem": {
      "requests": "6522422Ki",
      "requests_percent": 10,
      "limits": "10543260928",
      "limits_percent": 16
    },
    "cpu": {
      "requests": "1075m",
      "requests_percent": 12,
      "limits": "4500m",
      "limits_percent": 50
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "charlie",
    "mem": {
      "requests": "3634742Ki",
      "requests_percent": 5,
      "limits": "7586276608",
      "limits_percent": 12
    },
    "cpu": {
      "requests": "1075m",
      "requests_percent": 12,
      "limits": "3200m",
      "limits_percent": 35
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "delta",
    "mem": {
      "requests": "11499062Ki",
      "requests_percent": 18,
      "limits": "15639340288",
      "limits_percent": 24
    },
    "cpu": {
      "requests": "1253m",
      "requests_percent": 14,
      "limits": "6500m",
      "limits_percent": 73
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "echo",
    "mem": {
      "requests": "6870582Ki",
      "requests_percent": 11,
      "limits": "10899776768",
      "limits_percent": 17
    },
    "cpu": {
      "requests": "1975m",
      "requests_percent": 22,
      "limits": "4750m",
      "limits_percent": 53
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "foxtrot",
    "mem": {
      "requests": "1345078Ki",
      "requests_percent": 2,
      "limits": "5241660672",
      "limits_percent": 8
    },
    "cpu": {
      "requests": "725m",
      "requests_percent": 8,
      "limits": "2",
      "limits_percent": 22
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "golf",
    "mem": {
      "requests": "6114870Ki",
      "requests_percent": 9,
      "limits": "10178356480",
      "limits_percent": 16
    },
    "cpu": {
      "requests": "1875m",
      "requests_percent": 21,
      "limits": "4700m",
      "limits_percent": 52
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  },
  {
    "name": "hotel",
    "mem": {
      "requests": "5590582Ki",
      "requests_percent": 9,
      "limits": "22473958656",
      "limits_percent": 35
    },
    "cpu": {
      "requests": "1325m",
      "requests_percent": 14,
      "limits": "6100m",
      "limits_percent": 68
    },
    "gpu": {
      "requests": 0,
      "limits": 0
    }
  }
]


# References

* [jq](https://stedolan.github.io/jq/)
* [python3](https://pythonclock.org/)

