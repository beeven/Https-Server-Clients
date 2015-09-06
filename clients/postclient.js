

var request = require("request"),
	fs = require("fs");

request({
	url: "https://swdemo.gzeport.net:8443/CargoDeclaration/restful/custom/recive",
	method: "POST",
	json: true,
	headers :{
		"Content-Type":"application/json; charset=utf-8"
	},
	body: [{
		"MessageId": 13591,
    	"DateCreated": "2015-09-06T13:47:02+00:00",
	    "EntryNo": "515420151545087994",
	    "EportNo": "000000001023510475",
	    "NoticeTime": "2015-09-06T13:47:02+00:00",
	    "ReturnCode": "018",
	    "ReturnInfo": "直接申报成功2",
	    "ReturnType": "QP",
	    "TaskId": "T1907843510020150828f4ff60c09"
		}],
	cert : fs.readFileSync("../certs/swdemoClient.cer"),
	key: fs.readFileSync("../certs/swdemoClient.key"),
	ca: fs.readFileSync("../certs/swdemoCA.cer")
},function(err, res, body){
	if(err){
		console.error(err);
		return;
	}
	console.log(res.statusCode);
	console.log(body);
});
