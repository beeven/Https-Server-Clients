var gulp = require("gulp");
var Q = require("q");

gulp.task("makecert",function(){

});

gulp.task("prepare",function(){
	gulp.src("bower_components/bootstrap/dist/css/bootstrap.min.css")
		.pipe(gulp.dest("public/css/"));
	gulp.src("bower_components/bootstrap/dist/fonts/*")
		.pipe(gulp.dest("public/fonts/"));
})