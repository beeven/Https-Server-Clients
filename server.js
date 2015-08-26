var express = require("express"),
	bodyParser = require("body-parser"),
	app = express(),
	fs = require("fs"),
	https = require("https"),
	http = require("http"),
	Q = require("q"),
	request = require("request");

var options = {
	key: fs.readFileSync("certs/server.key"),
	cert: fs.readFileSync("certs/server.cer"),
	ca: [fs.readFileSync("certs/ca.cer")],
	rejectUnauthorized: true,
	requestCert: true,
	honorCipherOrder: true
}

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + "/public"));

var sendRequest = function(info){
	var deferred = Q.defer()
	var config = {};
	if(info.protocol == "https") {
		config.cert = fs.readFileSync("certs/client.cer");
		config.key = fs.readFileSync("certs/client.key");
		config.ca = fs.readFileSync("certs/ca.cer");
	}
	config.url = info.protocol + "://" + info.url;
	config.method = "POST";
	config.json = true;
	config.body = [{
		"MessageId": info.messageid,
    	"DateCreated": info.datecreated,
	    "EntryNo": info.entryno,
	    "EportNo": info.eportno,
	    "NoticeTime": info.noticetime,
	    "ReturnCode": info.returncode,
	    "ReturnInfo": info.returninfo,
	    "ReturnType": info.returntype,
	    "TaskId": info.taskid
	}]

	request(config,function(err, res, body){
		if(err) {
			deferred.reject(err);
			return;
		}
		deferred.resolve(body);
	});

	return deferred.promise;
}

app.post("/TestMessage",function(req,res){
	var info = req.body;
	if(typeof(info.url) === 'undefined' || info.url == null) {
		res.sendStatus(301);
		return;
	}
	sendRequest(info)
	.then(function(data){
		res.json({msg:"Success!", status: 0, response: data});
	})
	.catch(function(err){
		console.log(err);
		res.json({msg: err.toString(), status: 1});
	})
	.done()
});

app.get("/",function(req, res){
	res.send("World");
});


https.createServer(options, app).listen(8443);
http.createServer(app).listen(8080);