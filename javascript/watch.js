// gulpfile for automatic updating/rebuilding when constructing
// custom websites from scratch. 

var gulp                = require('gulp'),
    watch               = require('gulp-watch'),
    path                = require('path');


gulp.task('watch', function() {
  watch('./views/**/*.ejs', function() {
  });

  watch('./public/styles/**/*.css', function() {
    gulp.start('cssInject');
  });

  watch('./public/scripts/**/*.js', function() {
    gulp.start('scriptsRefresh');
  });

  watch('./public/images/**/*.jpg', function() {
    gulp.start('copyImages');
  });

  watch('./public/fonts/**/*', function() {
    gulp.start('copyFonts');
  });

  watch('./public/videos/**/*', function() {
    gulp.start('copyVideos');
  });
});

gulp.task('cssInject', ['styles']);

gulp.task('scriptsRefresh', ['scripts']);

gulp.task('copyImages', function() {
  return gulp.src('./public/images/**/*')
    .pipe(gulp.dest('./temp/images'));
});

gulp.task('copyFonts', function() {
  return gulp.src('./public/fonts/**/*')
    .pipe(gulp.dest('./temp/fonts'));
});

gulp.task('copyVideos', function() {
  return gulp.src('./public/videos/**/*')
    .pipe(gulp.dest('./temp/videos'));
});
