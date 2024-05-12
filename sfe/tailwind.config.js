

module.exports = {
        content: [
            'node_modules/preline/dist/*.js',
        ],
        plugins: [
          require("@tailwindcss/typography"),
          require("@tailwindcss/forms"),
          require("@tailwindcss/line-clamp"),
          require("tailwind-children"),
          require("tailwind-saasblocks"),
          require('preline/plugin'),
          require('flowbite/plugin'),
        ],
        
        
        theme: {
          extend: {
            fontFamily: {
              sans: ["Inter", ...defaultTheme.fontFamily.sans],
            },
          },
        },
      }

