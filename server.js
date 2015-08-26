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
	var deferred = Q.defer()
	var config = {};
	if(info.protocal == "https") {
		config.cert = fs.readFileSync("../certs/client.cer");
		config.key = fs.readFileSync("../certs/client.key");
		config.ca = fs.readFileSync("../certs/ca.cer");
	}

	config.url = info.protocal + info.addr;
	config.method = "POST";
	config.json = true;
	config.body = {}

	request(config,function(err, res, body){
		if(err) {
			deferred.reject(err);
			return;
		}
		deferred.resolve(body);
	});

	return deferred.promise;
}

app.post("/SendTestMsg",function(req,res){
	var info = req.body;
	if(typeof(info.addr) === 'undefined' || info.addr == null) {
		res.sendStatus(301);
		return;
	}
	sendRequest().then(function(){

	})
	.catch(function(err){

	})
	.done()
});

app.get("/",function(req, res){
	res.send("World");
});

https.createServer(options, app).listen(8443);
http.createServer(app).listen(8080);