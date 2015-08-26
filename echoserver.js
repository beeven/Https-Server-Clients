var express = require("express"),
	bodyParser = require("body-parser"),
	multer = require("multer"),
	app = express(),
	fs = require("fs"),
	https = require("https");

var options = {
	key: fs.readFileSync("certs/server.key"),
	cert: fs.readFileSync("certs/server.cer"),
	ca: [fs.readFileSync("certs/ca.cer")],
	rejectUnauthorized: true,
	requestCert: true,
	honorCipherOrder: true
}

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

var storage = multer.memoryStorage();
app.use("/avatar",multer({storage: storage}).single('avatar')); // for parsing multipart/form-data

app.all("*", function(req,res){
	res.json({"hello":"world", "info":{
		"url":req.path, 
		"method":req.method,
		"Content-Type": req.get("Content-Type"),
		"content": req.body,
		"query":req.query,
	}});
	console.log(req.headers);
	console.log(req.body);
	console.log(req.file)
});

https.createServer(options,app).listen(8043);
app.listen(8088);
