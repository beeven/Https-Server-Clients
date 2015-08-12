import requests
import json

payload = {"Hello":"PostContent"}
r = requests.post("https://localhost:8080/post",
	data=json.dumps(payload),
	headers={"Content-Type":"application/json"},
	cert=("client.cer","certs/client.key"),
	verify="certs/ca.cer"
)
print(r.text)

#r2 = requests.post("http://localhost:8080/avatar", files={'avatar':('hello.txt',open("hello.txt","rb"),"text/plain",{"Expires":0})})
#print(r2.text)

# r = requests.get("https://183.63.251.70/",cert=("client.cer","client.key"),verify="ca.cer")
# print(r.text)