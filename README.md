Https Server and Clients
=============

Https server in nodejs, requiring client certificates.

And https clients written in python, nodejs, c#, java.


## How to make certificates

### CA certificate
```bash
openssl genrsa -des3 -out ca.key 2048
openssl req -new -x509 -key ca.key -out ca.cer -days 1095
```

### Server certificate
```bash
openssl req -new -newkey rsa:2048 -nodes -out server.csr -keyout server.key -config server.cnf
​
openssl x509 -req -in server.csr -CA ca.cer -CAkey ca.key -out server.cer -days 1095 -set_serial 1002 -extfile server.cnf -extensions v3_req
```

### Client certificate
```bash
openssl req -new -newkey rsa:2048 -nodes -out client.csr -keyout client.key
openssl x509 -req -in client.csr -CA ca.cer -CAkey ca.key -out client.cer -days 1095 -set_serial 1003

openssl pkcs12 -export -inkey client.key -in client.cer -out client.pfx -CAfile ca.cer
```
