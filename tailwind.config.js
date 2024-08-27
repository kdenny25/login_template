/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
  content: [
      "./templates/**/*.html",
      "./templates/**/**/*.html",
      "./static/*.js",
      "./static/src/**/*.js",
      "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require("flowbite/plugin")
  ],
}

