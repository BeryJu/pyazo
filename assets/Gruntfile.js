module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    'npm-command': {
      install: {
        cmd: 'install',
      },
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      pyazo: {
        src: [
            'node_modules/clarity-icons/clarity-icons.min.js',
            'node_modules/jquery/dist/jquery.js',
            'js/*.js',
        ],
        dest: '../pyazo/static/app.min.js',
      },
    },
    cssmin: {
      pyazo: {
        files: [{
          src: [
              'node_modules/clarity-icons/clarity-icons.min.css',
              'node_modules/clarity-ui/clarity-ui.min.css',
              'css/*.css',
          ],
          dest: '../pyazo/static/app.min.css',
        }]
      }
    },
    copy: {
      images: {
        files: [
          { expand: true, cwd: 'img', src: ['*'], dest: '../pyazo/static/img/' },
        ]
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-npm-command');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['npm-command', 'uglify', 'cssmin', 'copy']);

};
