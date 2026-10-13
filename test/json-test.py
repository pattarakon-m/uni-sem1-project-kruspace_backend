import json

if __name__ == "__main__":
	obj = {
		"foo": (1,2),
		"bar": [3,4,5],
		"baz": 6,
		"hello": "world",
		"alice": {
			"foo": (1,2),
			"bar": [3,4,5],
		}
	}
	print(obj)
	jsonstr = json.dumps(obj)
	print(jsonstr)
	objparse = json.loads(jsonstr)
	print(objparse)

