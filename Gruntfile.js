module.exports = function(grunt) {
 
  grunt.registerTask('watch', [ 'watch' ]);
 
  grunt.initConfig({
    sass: {                              // Task
      dist: {                            // Target
	options: {                       // Target options
	  style: 'expanded'
	},
	files: {                         // Dictionary of files
	  'static/css/main.css': 'static/scss/main.scss',       // 'destination': 'source'
	}
      }
    },
    watch: {
      css: {
        files: ['static/scss/**/*.scss'],
        tasks: ['sass'],
      },
      livereload: {
        options: { livereload: true },
        files: ["static/css/main.css"],
      }
    }
  });
 
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
 
};
