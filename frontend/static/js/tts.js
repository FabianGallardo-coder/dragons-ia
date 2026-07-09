/**
 * Dragons & IA — tts.js
 * Text-to-Speech: Web Speech API (default) + Piper TTS backend (upgrade).
 * Persistencia en localStorage.
 */

const TTS = {
  enabled: true,
  usePiper: false,
  voice: null,
  rate: 1.0,
  voiceURI: '',
  _unlocked: false,

  init() {
    const saved = localStorage.getItem('dia_tts_config');
    if (saved) {
      try {
        const c = JSON.parse(saved);
        this.enabled = c.enabled ?? true;
        this.rate = c.rate ?? 1.0;
        this.voiceURI = c.voiceURI || '';
      } catch {}
    }

    if ('speechSynthesis' in window) {
      // Chrome: getVoices() devuelve [] en el primer llamado,
      // la lista real llega vía onvoiceschanged
      speechSynthesis.onvoiceschanged = () => this._loadVoices();
      this._loadVoices();

      // Chrome bloquea speak() sin interacción del usuario.
      // "Prewarm": apenas el usuario hace click/toca, desbloqueamos el API.
      const unlock = () => {
        if (this._unlocked) return;
        this._unlocked = true;
        speechSynthesis.cancel();
        const dummy = new SpeechSynthesisUtterance('');
        speechSynthesis.speak(dummy);
        document.removeEventListener('click', unlock);
        document.removeEventListener('keydown', unlock);
        document.removeEventListener('touchstart', unlock);
      };
      document.addEventListener('click', unlock);
      document.addEventListener('keydown', unlock);
      document.addEventListener('touchstart', unlock);
    }

    this.checkPiper();
  },

  _loadVoices() {
    const voices = speechSynthesis.getVoices();
    const spanish = voices.filter(v => v.lang.startsWith('es'));
    if (this.voiceURI) {
      this.voice = spanish.find(v => v.voiceURI === this.voiceURI);
    }
    if (!this.voice) {
      this.voice = spanish.find(v => v.lang.startsWith('es-MX'))
        || spanish.find(v => v.lang.startsWith('es-ES'))
        || spanish.find(v => v.lang.startsWith('es'))
        || voices[0]
        || null;
    }
  },

  async checkPiper() {
    try {
      const res = await fetch('/api/tts/status');
      if (res.ok) {
        const data = await res.json();
        this.usePiper = data.available && data.voice_exists;
      }
    } catch {
      this.usePiper = false;
    }
  },

  speak(text) {
    if (!this.enabled || !text) return;
    // Reintentar cargar voces si aún no hay (Chrome tardío)
    if (!this.voice && 'speechSynthesis' in window) {
      this._loadVoices();
    }
    if (this.usePiper) {
      this._speakPiper(text).catch(() => {
        this.usePiper = false;
        this._speakWebSpeech(text);
      });
    } else {
      this._speakWebSpeech(text);
    }
  },

  _speakWebSpeech(text) {
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(this._cleanText(text));
    u.lang = 'es-ES';
    u.rate = this.rate;
    if (this.voice) u.voice = this.voice;
    u.onerror = (e) => console.warn('TTS error:', e.error);
    speechSynthesis.speak(u);
  },

  async _speakPiper(text) {
    const res = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: this._cleanText(text) }),
    });
    if (!res.ok) throw new Error('Piper TTS error');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.onended = () => { URL.revokeObjectURL(url); this._onEnded(); };
    audio.play();
  },

  _cleanText(text) {
    return text
      .replace(/<[^>]+>/g, ' ')
      .replace(/```[\s\S]*?```/g, ' ')
      .replace(/https?:\/\/\S+/g, ' ')
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/[#*_~`>\-\[\]()!]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 2000);
  },

  stop() {
    if ('speechSynthesis' in window) speechSynthesis.cancel();
  },

  toggle() {
    this.enabled = !this.enabled;
    if (!this.enabled) this.stop();
    this._save();
    return this.enabled;
  },

  setRate(rate) {
    this.rate = Math.max(0.5, Math.min(2, rate));
    this._save();
  },

  setVoice(voiceURI) {
    this.voiceURI = voiceURI;
    this._loadVoices();
    this._save();
  },

  _save() {
    localStorage.setItem('dia_tts_config', JSON.stringify({
      enabled: this.enabled,
      rate: this.rate,
      voiceURI: this.voiceURI,
    }));
  },

  _onEnded() {},
};

document.addEventListener('DOMContentLoaded', () => TTS.init());
