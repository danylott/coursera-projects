import os
import tempfile
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--key", help="key for value in dict")
parser.add_argument("--val", help="value in dict")
args = parser.parse_args()
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
# storage_path = 'input.json'

if not os.path.exists(storage_path):
    with open(storage_path, 'w') as f:
        pass

storage = {}
with open(storage_path, 'r') as f:
    if os.stat(storage_path).st_size != 0:
        data = f.read()
        storage = json.loads(data)

if args.val:
    if args.key not in storage:
        storage[args.key] = [args.val]
    else:
        storage[args.key].append(args.val)
    with open(storage_path, 'w') as f:
        json.dump(storage, f)
else:
    if args.key in storage:
        print(', '.join(storage[args.key]))
    else:
        print(None)



