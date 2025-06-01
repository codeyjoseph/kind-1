from ruamel.yaml import YAML
import requests, time

def config(filepath):
	yaml = YAML()
	with open(filepath, 'r') as f:
		config = yaml.load(f)
	return config

def send_with_interval(message, url):
	response = requests.post(
		url,
		json={"message": message},
	)
	print(response.text)
	time.sleep(1)

filepath = "config/sender.yaml"
url = config(filepath)["backend"]
while True:
	print("Sending message to: ", url)
	send_with_interval("message from frontend", url)