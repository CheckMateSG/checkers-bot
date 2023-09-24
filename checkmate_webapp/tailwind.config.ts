import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      gridTemplateColumns:{
        sidebar: "250px auto",
        "sidebar-collapsed": "64px auto",
        // sidebar: "col-1 col-span-4",
        // "sidebar-collapsed": "col-1 col-span-1",
      }
    },
  },
  plugins: [],
}
export default config
