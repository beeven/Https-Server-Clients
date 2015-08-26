var gulp = require("gulp");
var Q = require("q");



gulp.task("prepare",function(){
	gulp.src("bower_components/bootstrap/dist/css/bootstrap.min.css")
		.pipe(gulp.dest("public/css/"));
	gulp.src("bower_components/bootstrap/dist/fonts/*")
		.pipe(gulp.dest("public/fonts/"));
	gulp.src("bower_components/bootstrap/dist/js/bootstrap.min.js")
		.pipe(gulp.dest("public/js/"));
	gulp.src("bower_components/moment/min/moment.min.js")
		.pipe(gulp.dest("public/js/"));
	gulp.src("bower_components/jquery/dist/jquery.min.*")
		.pipe(gulp.dest("public/js/"));
})
