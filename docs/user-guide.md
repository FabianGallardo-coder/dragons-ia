# User Guide

## Getting Started
1. **Visit** the live demo at [dragons-ia.onrender.com](https://dragons-ia.onrender.com) or deploy locally
2. **Create an account** — Register with username and password
3. **Configure AI** — Go to Configuración and choose your AI provider:
   - **Anthropic (Claude)**: Best quality, requires API key
   - **Ollama Cloud**: Good quality, requires API key
   - **Ollama Local**: Free, runs on your PC
4. **Create a character** — Choose race, class, and assign stats (Point Buy system)
5. **Choose a world** — Fantasía Medieval, Ciencia Ficción, Isekai, or Fantasía Oscura
6. **Start playing!** — The AI Dungeon Master narrates your adventure

## Game Features

### Actions
Type any action in the text input, or use Quick Actions:
- ⚔️ **Atacar** — Fight enemies
- 🛡️ **Defenderse** — Raise guard
- 🎒 **Bolsa** — Check inventory
- 🏃 **Huir** — Attempt escape

### Dice Rolling
Click any die (d4–d20) once per turn. Results are sent with your next action:
- **Nat 20** (Critical): ⚡ Epic success with visual effects
- **Nat 1** (Fumble): 💀 Total failure

### Character Status
- **HP bar**: Green → Yellow → Red as health decreases
- **XP bar**: Earn experience, level up every 100 XP
- **Turn counter**: Track your adventure progress

### AI Status Indicator
- ⚫ **Gray**: Idle
- 🟡 **Pulsating yellow**: AI is thinking
- 🟢 **Green**: Connected
- 🔴 **Red**: Error

### Voice Narration (TTS)
Enable voice narration for the DM's responses:
1. Go to **Configuración → Narración por Voz**
2. Toggle voice on/off, adjust speed, select voice
3. Or use the quick toggle in the game footer

**How it works:**
- Uses your browser's built-in speech synthesis (Web Speech API) by default
- If Piper TTS is installed on the server, it automatically upgrades to higher quality voice
- The first click on the page unlocks Chrome's speech synthesis (required by Chrome policy)
- If Piper fails, it falls back to Web Speech API automatically

### Saving
- Games auto-save after each action
- Manual save with 💾 **Guardar** button
- Exit with 🚪 **Salir** (confirms first)

## AI Provider Setup

### Anthropic
1. Create account at [console.anthropic.com](https://console.anthropic.com)
2. Generate an API Key
3. In-game: **Configuración → Anthropic → paste API Key**

### Ollama Cloud
1. Register at [ollama.com](https://ollama.com)
2. Get API Key from **Settings → API Keys**
3. In-game: **Configuración → Ollama Cloud → paste API Key → click "🔄 Cargar modelos"** para obtener la lista de modelos disponibles desde la API oficial
4. Seleccioná un modelo de la lista cargada dinámicamente (35+ modelos disponibles)

### Ollama Local (Free)
1. Install Ollama from [ollama.com/download](https://ollama.com/download)
2. Pull a model: `ollama pull dolphin-mistral`
3. In-game: **Configuración → Ollama Local → choose model**
4. The system will auto-detect your installed models and RAM

## ASCII Art
The game shows ASCII art scenes that change with each action:
- **Scenarios**: Each action triggers a scene based on keywords in the AI's narrative (battle, victory, rest, exploration, etc.)
- **Worlds**: Each world has its own set of art and a FIGlet title font
- **Full-width**: Art spans the full game width for maximum visibility

## Tips
- Describe your actions in detail for richer narration
- Use dice for important actions (combat, persuasion, stealth)
- Different worlds have different fonts and tones
- Your API key stays in your browser — it's never sent to our server
- Click anywhere on the page first to unlock voice narration (Chrome policy)
