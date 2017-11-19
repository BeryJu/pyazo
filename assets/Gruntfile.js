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
            'node_modules/dropzone/dist/dropzone.js',
            'node_modules/clarity-icons/clarity-icons.min.js',
            'node_modules/jquery/dist/jquery.js',
            'js/*.js',
        ],
        dest: '../pyazo/static/js/app.min.js',
      },
    },
    cssmin: {
      pyazo: {
        files: [{
          src: [
              'node_modules/clarity-icons/clarity-icons.min.css',
              'node_modules/clarity-ui/clarity-ui.min.css',
              'node_modules/font-awesome/css/font-awesome.min.css',
              'node_modules/dropzone/dist/dropzone.css',
              'css/*.css',
          ],
          dest: '../pyazo/static/css/app.min.css',
        }]
      }
    },
    copy: {
      custom_elements: {
        files: [
          { src: ['node_modules/@webcomponents/custom-elements/custom-elements.min.js'],
            dest: '../pyazo/static/js/custom-elements.min.js'}
        ]
      },
      raven: {
        files: [
          { src: ['node_modules/raven-js/dist/raven.min.js'],
            dest: '../pyazo/static/js/raven.min.js'}
        ]
      },
      images: {
        files: [
          { expand: true, cwd: 'img', src: ['*'], dest: '../pyazo/static/img/' },
        ]
      },
      fonts: {
        files: [
          { expand: true, cwd: 'node_modules/font-awesome/fonts/', src: ['*'], dest: '../pyazo/static/fonts/' },
        ]
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-npm-command');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['uglify', 'cssmin', 'copy']);

};
