var paths = {
    js : 'app/static/js/mainJobs.js'
}

module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            all: {
                src: [paths.js],
                options: {
                    jshintrc: true
                }
            }
        },

	watch: {
            dev: {
                files: [paths.js],
                tasks: ['jshint', 'watch'],
                options: {
                    spawn: false,
                    livereload: true,
                },
            },
        },


     });

 
    require('load-grunt-tasks')(grunt);

    grunt.registerTask('default', ['jshint']);
    grunt.registerTask('dev', ['jshint', 'watch']);
};
