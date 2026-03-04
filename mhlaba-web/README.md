# MHLABA Web Interface

A modern, KimiCode-like web interface for MHLABA AI Assistant.

## Features

- 🎨 **Modern Dark Theme** - Clean, professional interface inspired by KimiCode
- 💬 **Real-time Chat** - Smooth messaging experience with markdown support
- 🤖 **Multiple AI Providers** - Support for OpenAI (GPT-3.5, GPT-4) and Anthropic (Claude)
- 💾 **Local Storage** - Conversations saved locally in your browser
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔒 **Privacy First** - API keys stored only in your browser's localStorage

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the web directory:
```bash
cd mhlaba-web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

### Building for Production

```bash
npm run build
```

The build output will be in the `dist` directory.

## Configuration

### API Keys

The first time you use MHLABA, you'll need to configure your AI provider API key:

1. Click the **Settings** button (gear icon)
2. Select your preferred provider (OpenAI or Anthropic)
3. Enter your API key
4. Choose your preferred model
5. Click **Save Settings**

Your API key is stored only in your browser's localStorage and is never sent to any server other than the AI provider's API.

### Getting API Keys

**OpenAI:**
- Visit https://platform.openai.com/api-keys
- Create a new API key
- Copy and paste it into the settings

**Anthropic:**
- Visit https://console.anthropic.com/settings/keys
- Create a new API key
- Copy and paste it into the settings

## Deployment

### Deploy to Netlify

#### Option 1: Deploy via Netlify CLI

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Login to Netlify:
```bash
netlify login
```

3. Deploy:
```bash
cd mhlaba-web
netlify deploy --prod --dir=dist
```

#### Option 2: Deploy via Git

1. Push your code to GitHub/GitLab/Bitbucket

2. Connect your repository to Netlify:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose your Git provider and repository
   - Build settings will be auto-detected from `netlify.toml`
   - Click "Deploy site"

#### Option 3: Manual Deploy

1. Build the project:
```bash
cd mhlaba-web
npm run build
```

2. Go to https://app.netlify.com/drop

3. Drag and drop the `dist` folder

## Project Structure

```
mhlaba-web/
├── public/
│   └── favicon.svg
├── src/
│   ├── App.jsx       # Main application component
│   ├── App.css       # Styles with KimiCode-like theme
│   └── main.jsx      # Entry point
├── index.html        # HTML template
├── package.json      # Dependencies
├── vite.config.js    # Vite configuration
├── netlify.toml      # Netlify deployment config
└── README.md         # This file
```

## Customization

### Changing the Theme

Edit `src/App.css` to customize colors:

```css
:root {
  --bg-primary: #0d0d0d;      /* Main background */
  --bg-secondary: #1a1a1a;    /* Sidebar background */
  --accent-primary: #6366f1;   /* Primary accent color */
  --accent-secondary: #a855f7; /* Secondary accent color */
  /* ... more variables */
}
```

### Changing the Name

To change "MHLABA" to something else:

1. Edit `index.html` - Update the `<title>` tag
2. Edit `src/App.jsx` - Update all instances of "MHLABA"
3. Edit `public/favicon.svg` - Update the logo

## Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message
- `Esc` - Close settings modal

## Troubleshooting

### "Please set your API key" error
- Click the Settings button and enter your API key
- Make sure you're using the correct key for your selected provider

### Messages not sending
- Check that your API key is valid
- Verify you have internet connection
- Check browser console for error messages

### Build fails
- Make sure you're using Node.js 18 or higher
- Delete `node_modules` and run `npm install` again

## License

Personal use only.

---

Built with ❤️ using React + Vite
