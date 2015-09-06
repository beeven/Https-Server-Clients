#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import json

payload = [{
        "MessageId": 13591,
        "DateCreated": "2015-09-06T13:13:04+00:00",
        "EntryNo": "515420151545087994",
        "EportNo": "000000001023510475",
        "NoticeTime": "2015-09-06T13:13:04+00:00",
        "ReturnCode": "008",
        "ReturnInfo": "直接申报成功2",
        "ReturnType": "QP",
        "TaskId": "T1907843510020150827f4ff60bc0"
    }];
r = requests.post("https://swdemo.gzeport.net:8443/CargoDeclaration/restful/custom/recive",
	#data=json.dumps(payload, ensure_ascii=False),
    json=payload,
	headers={"Content-Type":"application/json; charset=utf-8"},
	cert=("../certs/swdemoClient.cer","../certs/swdemoClient.key"),
	verify="../certs/swdemoCA.cer"
)
print(r.text)

#r2 = requests.post("http://localhost:8080/avatar", files={'avatar':('hello.txt',open("hello.txt","rb"),"text/plain",{"Expires":0})})
#print(r2.text)

# r = requests.get("https://183.63.251.70/",cert=("client.cer","client.key"),verify="ca.cer")
# print(r.text)