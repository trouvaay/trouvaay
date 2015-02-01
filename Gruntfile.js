module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
	sass: {
		dist: {
			options: {
				style: 'expanded'
			},
	files: {
		'static/css/main.css': 'static/css/main.scss',
	}
		}
	},
	uncss: {
		dist: {
			src: ['http://127.0.0.1:8000/', 'http://127.0.0.1:8000/accounts/password/reset/', 'http://127.0.0.1:8000/piece/landon-coffee-table/', 'http://127.0.0.1:8000/about/', 'http://127.0.0.1:8000/category/?type=seats', 'http://127.0.0.1:8000/login/', 'http://127.0.0.1:8000/signup/', ],
	//src: ['templates/400.html', 'templates/403.html', 'templates/404.html', 'templates/500.html', 'templates/custom.html', 'templates/_base.html', ],
	dest: 'static/css/main.min.css'
		},

	},
	ucss: {
		target: {
			pages: {
				crawl: 'http://localhost:8000/'
			},
			css: ['static/css/main.css']
		}
	},
	cssmin: {
		css: {
			src: 'static/css/main.min.css',
			dest: 'static/css/main.min.css',
		}
	},

	});

	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-uncss');
	grunt.loadNpmTasks('grunt-ucss');
	grunt.loadNpmTasks('grunt-contrib-cssmin');

	grunt.registerTask('default', ['sass']);
	grunt.registerTask('min', ['uncss', 'cssmin:css']);

};
