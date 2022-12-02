import requests
url = "http://127.0.0.1:8000/gojo/post/"
data = {"author":"ko0", "content": "This is a test post from Ko0!"}
rsp = requests.post(url=url, json=data)
with open("file.html", 'wb') as fl:
    fl.write(rsp.content)
    fl.close()
print(rsp.status_code, rsp.content)

"""
SIGN UP TEMPLATE

{
	"main":{
		"username":"meron",
		"password":"random",
		"email":"meron@gmail.com"
	},
	"profile":{
		"first_name":"meron",
		"last_name":"abebe",
		"birth_date":"1999-03-19",
		"country":"ET"
	}
}
"""

"""
LOGIN TEMPLATE

{
		"username":"meron",
		"password":"random",
}
"""