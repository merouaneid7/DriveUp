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
          require("@tailwindcss/typography"),
          require("@tailwindcss/forms"),
          require("@tailwindcss/line-clamp"),
          require("tailwind-children"),
          require("tailwind-saasblocks"),
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
        ],
        theme: {
          extend: {
            fontFamily: {
              sans: ["Inter", ...defaultTheme.fontFamily.sans],
            },
          },
        },
      }

const eggshellDelightsTheme = require("tailwind-saasblocks/themes/eggshell-delights.theme");
const midnightEnvyTheme = require("tailwind-saasblocks/themes/midnight-envy.theme");

/** @type {import('tailwindcss').Config} */
