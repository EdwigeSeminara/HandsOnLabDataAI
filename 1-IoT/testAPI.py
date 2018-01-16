import sys
import requests
import json

def main():
    with open("folds.json") as file:
        data = json.load(file)
    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/1a79282cf714419ca44678495dde9834/services/345bdff689c548a9bc60df6d757c40c8/execute?api-version=2.0&details=true'
    api_key = 'D0hMXaSOYHwKxk8FRnbAfUuGBOX4jwMESwbyfX3Qt/WmIiN9YjDHjka0oy1vhx6C5l9zEosuEW/e4QOBleCdCQ=='
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}


    resp = requests.post(url, body, headers=headers)
    print resp.text


if __name__ == '__main__':
    main()