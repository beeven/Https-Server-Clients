var express = require("express"),
	bodyParser = require("body-parser"),
	app = express(),
	fs = require("fs"),
	https = require("https"),
	Q = require("q"),
	request = require("request");

var options = {
	key: fs.readFileSync("certs/server.key"),
	cert: fs.readFileSync("certs/LocalTestServer.cer"),
	ca: [fs.readFileSync("certs/ca.cer")],
	rejectUnauthorized: true,
	requestCert: true,
	honorCipherOrder: true
}

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true })); 

var sendRequest = function(info){
	
}

app.post("/recipt",function(req,res){
	var info = req.body;
	if(typeof(info.addr) === 'undefined' || info.addr == null) {
		res.sendStatus(301);
		return;
	}
	//console.log(body.Hello);
	//res.sendStatus(200);
});

app.get("/",function(req, res){
	res.send("World");
});

https.createServer(options, app).listen(8080);