import json

def data_from_jsom(file):
    with open(file, 'r') as f:
        json_data = f.read()
    data = json.loads(json_data)
    print(data)

if __name__ == "__main__":
	data_from_jsom("ciga_conf.json")