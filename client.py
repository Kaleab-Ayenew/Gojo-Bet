import requests
url = "http://127.0.0.1:8000/gojo/post/"
data = {"author":"kalish", "content": "This is a test post from the BOSS"}
rsp = requests.post(url=url, json=data)
with open("file.html", 'wb') as fl:
    fl.write(rsp.content)
    fl.close()
print(rsp.status_code, rsp.content)

