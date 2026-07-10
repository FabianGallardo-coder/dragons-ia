# Workflows and Features

The Dragons-IA project offers a rich set of features centered around an AI-driven text-based adventure game experience. The key workflows and features include:

## Core Gameplay Loop

1.  **User Interaction:** Players interact with the game through text commands entered via the frontend interface.
2.  **AI-Driven Narrative (Dungeon Master):** The backend's Dungeon Master service interprets player commands, generates narrative responses, describes scenes, and manages NPC interactions. It aims to create dynamic and evolving storylines based on player actions.
3.  **State Management:** The game state, including player progress, inventory, and world status, is managed by the backend and persisted.
4.  **Dynamic Content Generation:** AI services are leveraged to generate descriptive text, dialogue, and potentially even game events, ensuring a unique experience for each player.

## Key Features

*   **Immersive Storytelling:** The core focus is on delivering an engaging narrative experience through AI-generated text and descriptive language.
*   **Text-to-Speech (TTS):** An integrated TTS system (likely using Piper) converts the game's text output into spoken audio, significantly enhancing immersion. This feature is configurable and appears to support different voices and languages.
*   **ASCII Art Integration:** For visual flair, the game incorporates ASCII art, potentially generated dynamically or pre-defined, to represent scenes, characters, or items. Files like `scripts/ascii_art.py` and frontend components related to `ascii_manager.js` suggest this feature is actively developed.
*   **User Authentication and Persistence:** Users can create accounts, log in, and save their game progress, allowing them to resumeT their adventures later. JWTs are used for authentication, with logic for handling expiry and session status.
*   **Game Customization and Settings:** The frontend includes configuration pages (`frontend/config.html`) where users can likely adjust game settings, audio options, and potentially AI parameters.
*   **AI Model Management (Ollama):** The backend includes logic for detecting and interacting with AI models via Ollama, including system detection and fallback mechanisms for different models and environments. This allows for flexibility in leveraging local or cloud-based AI capabilities.
*   **Testing Frameworks:** The project supports both backend testing with `pytest` and frontend testing with Node.js-based tools, ensuring code quality and stability.

## AI and Immersion Enhancements

Recent development activity highlights a strong emphasis on enhancing immersion:

*   **Advanced Immersion Components:** The addition of numerous JavaScript files in `frontend/static/js/immersion/` (e.g., `animation_manager.js`, `audio_manager.js`, `cinematic_mode.js`) indicates a push towards richer visual and auditory experiences within the game.
*   **Dungeon Master Tone and Rules:** Updates to the Dungeon Master service (`backend/services/dungeon_master.py`) suggest nuanced control over narrative tone and world-specific rules, allowing for more tailored game experiences.
*   **TTS Sync and Management:** Components like `tts_sync.js` point to efforts in synchronizing TTS playback with the game's narrative flow.

These features collectively aim to create a deeply engaging and interactive AI-powered role-playing experience.