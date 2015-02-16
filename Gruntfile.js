module.exports = function(grunt) {
 
  grunt.registerTask('watch', [ 'watch' ]);
 
  grunt.initConfig({
    // concat: {
    //   js: {
    //     options: {
    //       separator: ';'
    //     },
    //     src: [
    //       'javascript/*.js'
    //     ],
    //     dest: 'public/js/main.min.js'
    //   },
    // },
    // uglify: {
    //   options: {
    //     mangle: false
    //   },
    //   js: {
    //     files: {
    //       'public/js/main.min.js': ['public/js/main.min.js']
    //     }
    //   }
    // },
    coffee: {
      glob_to_multiple: {
        expand: true,
        flatten: true,
        cwd: 'catalog/static/scripts',
        src: ['*.coffee'],
        dest: 'catalog/static/scripts',
        ext: '.js'
      },

      blob_to_multiple: {
        expand: true,
        flatten: true,
	files: {
		"dex/static/js/dex.js": "dex/static/coffee/dex.coffee",
		"bd/static/scripts/*.js": "bd/static/scripts/*.coffee",
	}
	/*
        cwd: 'bd/static/scripts',
        src: ['*.coffee'],
        dest: 'bd/static/scripts',
        ext: '.js'
	*/
      }
    },
    
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
      // js: {
      //   files: ['javascript/*.js'],
      //   tasks: ['concat:js', 'uglify:js'],
      //   options: {
      //     livereload: true,
      //   }
      // },
      css: {
        files: ['static/scss/**/*.scss'],
        tasks: ['sass'],
      },
      coffee: {
        files: ['catalog/static/scripts/**/*.coffee', 'bd/static/scripts/**/*.coffee', 'dex/static/coffee/**/*.coffee'],
        tasks: ['coffee:glob_to_multiple', 'coffee:blob_to_multiple'],
      },
      livereload: {
        options: { livereload: true },
        files: ["static/css/main.css", "catalog/static/scripts/main.js", "bd/static/scripts/navigation.js", "dex/static/css/dex.css"]
      }
    }
  });
 
  // grunt.loadNpmTasks('grunt-contrib-concat');
  // grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-sass');
  //grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');
 
};
