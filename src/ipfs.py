import json
import requests
from requests.structures import CaseInsensitiveDict

api_key = "api key here"
api_endpoint = "https://ipfs.blockfrost.io/api/v0"
header = {'project_id': '{0}'.format(api_key) }

######### API Request Functions #########

# send file to blockfrost IPFS...
def upload_file(file_path):
	url = api_endpoint + "/ipfs/add"
	headers = CaseInsensitiveDict()
	headers["Content-Length"] = "0"
	headers["project_id"] = api_key

	files = {'file': open(file_path, 'rb')}

	resp = requests.post(url, files=files, headers=headers)

	return resp.json()

# pin file to prevent garbage collection...
def pin_ipfs(ipfs_hash):
	url = api_endpoint + "/ipfs/pin/add/{0}".format(ipfs_hash)
	headers = CaseInsensitiveDict()
	headers["project_id"] = api_key

	resp = requests.post(url, headers=headers)

	print("pinned: " + str(resp.json()))
	return resp.json()


# remove file from IPFS pinning...
def unpin_ipfs(ipfs_hash):
	url = api_endpoint + "/ipfs/pin/remove/{0}".format(ipfs_hash)
	headers = CaseInsensitiveDict()
	headers["project_id"] = api_key

	resp = requests.post(url, headers=headers)

	print("unpinned: " + str(resp.json()))
	return resp.json()


# Upload image and pin it...
def upload_image(png_path):
	result = upload_file(png_path)
	result = pin_ipfs(result['ipfs_hash'])
	return result