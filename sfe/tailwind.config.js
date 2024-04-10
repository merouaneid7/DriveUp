module.exports = {

          plugins: [
              require('flowbite/plugin')
          ]
      
      }

module.exports = {

          content: [
              "./node_modules/flowbite/**/*.js"
          ]
      
      }

module.exports = {
        content: [
          // './src/**/*.{html,js}',
            'node_modules/preline/dist/*.js',
        ],
        plugins: [
          // require('@tailwindcss/forms'),
            require('preline/plugin'),
        ],
        plugins: [
          require('flowbite/plugin')({
              charts: true,
          }),
          // ... other plugins
        ]
      }

      