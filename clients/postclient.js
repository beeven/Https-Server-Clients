var request = require("request"),
	fs = require("fs");

request({
	url: "https://localhost:8043/recipt",
	method: "POST",
	json: true,
	body: {"Hello":"World"},
	cert : fs.readFileSync("../certs/client.cer"),
	key: fs.readFileSync("../certs/client.key"),
	ca: fs.readFileSync("../certs/ca.cer")
},function(err, res, body){
	if(err){
		console.error(err);
		return;
	}
	console.log(res.statusCode);
	console.log(body);
});
