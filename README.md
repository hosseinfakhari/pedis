### pedis

[Redis](https://redis.io) like database in Python.

#### installing

```
$ pip install pedis
```

Alternatively, you can install from git:

```
$ git clone https://github.com/hosseinfakhari/pedis
$ cd pedis
$ python setup.py install
```

#### running

by default, the pedis server runs on localhost:63790.

the following options are supported:

```
Usage: pedis.py [options]

Options:
  -h, --help            show this help message and exit
  -d, --debug           Log debug messages.
  -e, --errors          Log error messages only.
  -t, --use-threads     Use threads instead of gevent.
  -H HOST, --host=HOST  Host to listen on.
  -m MAX_CLIENTS, --max-clients=MAX_CLIENTS
                        Maximum number of clients.
  -p PORT, --port=PORT  Port to listen on.
  -l LOG_FILE, --log-file=LOG_FILE
                        Log file.
  -x EXTENSIONS, --extension=EXTENSIONS
                        Import path for Python extension module(s).
```

to run with debug logging on port 63790, for example:

```
$ pedis.py -d -p 63790
```

#### docker

pedis ships with a [Dockerfile](https://github.com/semilanceata/pedis/blob/master/Dockerfile)
. The dockerfile setups
up a volume at `/var/lib/pedis` and exposes port `63790`.


building:

```console
$ docker build -t pedis .
$ docker run -d -p 63790:63790 -v pedis-logs:/var/lib/pedis pedis
```

#### usage

the server is capable of storing the following data-types natively:

* strings and/or binary data
* numerical values
* null
* lists (may be nested)
* dictionaries (may be nested)

```python

from pedis import Client

client = Client()
client.set('key', {'name': 'Hossein', 'pets': ['jessie', 'feighsho']})

print(client.get('key'))
{'name': 'Hossein', 'pets': ['jessie', 'feighsho']}
```
