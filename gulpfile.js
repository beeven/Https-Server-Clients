var gulp = require("gulp"),
		shell = require("gulp-shell");
var Q = require("q");

gulp.task("makecert",shell.task([
	"openssl genrsa -out ca.key 2048",
	"openssl req -new -x509 -key ca.key -out ca.cer -days 1095",
	"openssl req -new -newkey rsa:2048 -nodes -out server.csr -keyout server.key -config server.cnf",
	"openssl x509 -req -in server.csr -CA ca.cer -CAkey ca.key -out server.cer -days 1095 -set_serial 1002 -extfile server.cnf -extensions v3_req",
	"openssl req -new -newkey rsa:2048 -nodes -out client.csr -keyout client.key",
	"openssl x509 -req -in client.csr -CA ca.cer -CAkey ca.key -out client.cer -days 1095 -set_serial 1003",
	"openssl pkcs12 -export -inkey client.key -in client.cer -out client.pfx -CAfile ca.cer"
]));

gulp.task("prepare",function(){
	gulp.src("bower_components/bootstrap/dist/css/bootstrap.min.css")
		.pipe(gulp.dest("public/css/"));
	gulp.src("bower_components/bootstrap/dist/fonts/*")
		.pipe(gulp.dest("public/fonts/"));
})
