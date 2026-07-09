const AudioManager = {
    _initialized: false,
    _enabled: true,
    _audioCtx: null,
    _masterGain: null,
    _ambienceGain: null,
    _sfxGain: null,
    _musicGain: null,
    _reverbNode: null,
    _currentScene: null,
    _ambienceNodes: [],
    _musicNodes: [],
    _musicInterval: null,
    _ambienceInterval: null,
    _sfxTimeout: null,
    _crossfading: false,

    SCENE_CHORDS: {
        tavern:   { notes: [261.63, 293.66, 329.63], pattern: [0,1,2,1], type: 'triangle', rate: 0.6, lfo: 0.3 },
        forest:   { notes: [392, 349.23, 329.63, 261.63], pattern: [0,2,1,3], type: 'sine', rate: 1.0, lfo: 0.2 },
        dungeon:  { notes: [130.81, 155.56, 196, 155.56], pattern: [0,1,2,1], type: 'sawtooth', rate: 0.4, lfo: 0.5 },
        castle:   { notes: [261.63, 329.63, 392, 293.66], pattern: [0,2,3,1], type: 'triangle', rate: 0.5, lfo: 0.2 },
        village:  { notes: [293.66, 329.63, 392, 349.23], pattern: [0,1,2,0], type: 'sine', rate: 0.7, lfo: 0.15 },
        city:     { notes: [329.63, 293.66, 392, 440], pattern: [0,1,2,3], type: 'triangle', rate: 0.6, lfo: 0.2 },
        mountain: { notes: [220, 261.63, 329.63, 392], pattern: [0,1,2,3], type: 'sine', rate: 0.5, lfo: 0.3 },
        library:  { notes: [261.63, 329.63, 392, 523.25], pattern: [0,2,0,3], type: 'sine', rate: 0.4, lfo: 0.1 },
        temple:   { notes: [392, 440, 493.88, 523.25], pattern: [0,2,1,2], type: 'sine', rate: 0.3, lfo: 0.15 },
        beach:    { notes: [392, 523.25, 587.33, 659.25], pattern: [0,1,0,2], type: 'sine', rate: 0.5, lfo: 0.2 },
        cave:     { notes: [146.83, 130.81, 110, 130.81], pattern: [0,1,2,1], type: 'sawtooth', rate: 0.3, lfo: 0.6 },
        battle:   { notes: [196, 233.08, 261.63, 311.13], pattern: [0,1,2,1], type: 'square', rate: 1.2, lfo: 0.4 },
        boss:     { notes: [130.81, 164.81, 196, 164.81], pattern: [0,1,2,1], type: 'sawtooth', rate: 0.8, lfo: 0.7 },
        mystery:  { notes: [392, 370, 349.23, 330], pattern: [0,1,2,1], type: 'sine', rate: 0.3, lfo: 0.3 },
        epic:     { notes: [220, 277.18, 329.63, 440], pattern: [0,2,1,3], type: 'triangle', rate: 0.6, lfo: 0.25 },
        sad:      { notes: [207.65, 174.61, 207.65, 261.63], pattern: [0,1,0,2], type: 'sine', rate: 0.3, lfo: 0.2 },
        tension:  { notes: [155.56, 164.81, 185, 196], pattern: [0,1,0,2], type: 'sawtooth', rate: 0.7, lfo: 0.5 },
        adventure:{ notes: [261.63, 293.66, 392, 349.23], pattern: [0,1,2,3], type: 'triangle', rate: 0.8, lfo: 0.2 },
        peaceful: { notes: [329.63, 392, 440, 523.25], pattern: [0,1,2,1], type: 'sine', rate: 0.4, lfo: 0.1 },
    },

    init() {
        if (this._initialized) return;
        this._initialized = true;
        if (window.SoundFontLoader) {
            SoundFontLoader.load().catch(() => {});
        }
    },

    async _ensureContext() {
        if (!this._audioCtx) {
            this._audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            this._reverbNode = this._buildReverb(2);
            this._masterGain = this._audioCtx.createGain();
            this._masterGain.gain.value = 0.3;
            this._masterGain.connect(this._audioCtx.destination);

            this._musicGain = this._audioCtx.createGain();
            this._musicGain.gain.value = 0.1;
            this._musicGain.connect(this._reverbNode);
            this._reverbNode.connect(this._masterGain);

            this._ambienceGain = this._audioCtx.createGain();
            this._ambienceGain.gain.value = 0.08;
            this._ambienceGain.connect(this._masterGain);

            this._sfxGain = this._audioCtx.createGain();
            this._sfxGain.gain.value = 0.2;
            this._sfxGain.connect(this._masterGain);
        }
        if (this._audioCtx.state === 'suspended') {
            await this._audioCtx.resume();
        }
    },

    _buildReverb(duration) {
        const ctx = this._audioCtx;
        const len = ctx.sampleRate * duration;
        const buf = ctx.createBuffer(2, len, ctx.sampleRate);
        for (let ch = 0; ch < 2; ch++) {
            const data = buf.getChannelData(ch);
            for (let i = 0; i < len; i++) {
                data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ctx.sampleRate * 0.3));
            }
        }
        const node = ctx.createConvolver();
        node.buffer = buf;
        return node;
    },

    apply(sceneData) {
        if (!this._enabled) return;
        if (!sceneData) return;

        const scene = sceneData.scene || 'forest';
        this._ensureContext().then(() => {
            const isNew = scene !== this._currentScene;
            this._currentScene = scene;

            if (isNew) {
                this._crossfadeMusic(sceneData.music || 'adventure');
                this._stopAmbience();
                this._playSceneAmbience(sceneData);
            }
        });
    },

    _playSceneAmbience(sceneData) {
        const ambiences = sceneData.ambience || [];
        ambiences.forEach(a => this._playAmbienceLoop(a));
    },

    _crossfadeMusic(track) {
        if (this._crossfading) return;
        this._crossfading = true;

        const oldGain = this._musicGain.gain.value;
        const now = this._audioCtx.currentTime;

        this._musicGain.gain.setValueAtTime(oldGain, now);
        this._musicGain.gain.linearRampToValueAtTime(0, now + 1.5);
        this._stopMusic();

        setTimeout(() => {
            this._playMusicLoop(track);
            const now2 = this._audioCtx.currentTime;
            this._musicGain.gain.setValueAtTime(0, now2);
            this._musicGain.gain.linearRampToValueAtTime(0.1, now2 + 1.5);
            this._crossfading = false;
        }, 1800);
    },

    playMusic(track) {
        this._ensureContext().then(() => {
            this._crossfadeMusic(track);
        });
    },

    stopMusic() {
        this._stopMusic();
        if (this._musicInterval) {
            clearInterval(this._musicInterval);
            this._musicInterval = null;
        }
    },

    playSFX(sfx) {
        if (!this._enabled) return;
        this._ensureContext().then(() => {
            this._synth(sfx);
        });
    },

    playAmbience(ambiences) {
        if (!this._enabled) return;
        this._ensureContext().then(() => {
            ambiences.forEach(a => this._playAmbienceLoop(a));
        });
    },

    stopAll() {
        this.stopMusic();
        this._stopAmbience();
        if (this._sfxTimeout) {
            clearTimeout(this._sfxTimeout);
            this._sfxTimeout = null;
        }
    },

    setEnabled(enabled) {
        this._enabled = enabled;
        if (!enabled) this.stopAll();
    },

    trigger(event) {
        if (!this._enabled) return;
        const sfxMap = {
            hit: 'sword', magic: 'magic', death: 'monster', victory: 'bell',
            door: 'door', water: 'water', fire: 'fire', thunder: 'thunder',
            step: 'footsteps', heart: 'heartbeat',
        };
        const sfx = sfxMap[event];
        if (sfx) this.playSFX(sfx);
    },

    _stopMusic() {
        this._musicNodes.forEach(n => {
            try { n.stop(); } catch (e) { }
        });
        this._musicNodes = [];
        if (this._musicInterval) {
            clearInterval(this._musicInterval);
            this._musicInterval = null;
        }
    },

    _stopAmbience() {
        this._ambienceNodes.forEach(n => {
            try { n.stop(); } catch (e) { }
        });
        this._ambienceNodes = [];
        if (this._ambienceInterval) {
            clearInterval(this._ambienceInterval);
            this._ambienceInterval = null;
        }
    },

    _playNote(freq, startTime, dur, type, lfoDepth) {
        const ctx = this._audioCtx;
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = type || 'sine';
        osc.frequency.setValueAtTime(freq, startTime);

        if (lfoDepth && lfoDepth > 0) {
            const lfo = ctx.createOscillator();
            const lfoGain = ctx.createGain();
            lfo.frequency.value = 4 + Math.random() * 2;
            lfoGain.gain.value = lfoDepth * 5;
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            lfo.start(startTime);
            lfo.stop(startTime + dur);
            this._musicNodes.push(lfo);
        }

        g.gain.setValueAtTime(0, startTime);
        g.gain.linearRampToValueAtTime(0.25, startTime + 0.05);
        g.gain.linearRampToValueAtTime(0.15, startTime + dur * 0.6);
        g.gain.exponentialRampToValueAtTime(0.001, startTime + dur);

        osc.connect(g);
        g.connect(this._musicGain);
        osc.start(startTime);
        osc.stop(startTime + dur);
        this._musicNodes.push(osc);
    },

    _playMusicLoop(track) {
        if (window.SoundFontLoader?.isLoaded()) {
            SoundFontLoader.playChord(track);
        }
        const chords = this.SCENE_CHORDS[track] || this.SCENE_CHORDS.adventure;
        const ctx = this._audioCtx;
        const bpm = chords.rate * 2;
        const beatDur = 60 / bpm;
        const pattern = chords.pattern;

        const scheduleBeat = () => {
            if (!this._enabled) return;
            const now = ctx.currentTime;

            for (let i = 0; i < pattern.length; i++) {
                const idx = pattern[i];
                const freq = chords.notes[idx % chords.notes.length];
                const offset = i * beatDur * 0.9;
                const noteDur = beatDur * 0.8;
                const type = i % 2 === 0 ? chords.type : 'sine';
                this._playNote(freq, now + offset, noteDur, type, chords.lfo);
            }

            if (chords.notes.length >= 3) {
                const bassFreq = chords.notes[0] * 0.5;
                this._playNote(bassFreq, now, beatDur * 2.5, 'sine', 0);
            }
        };

        scheduleBeat();
        this._musicInterval = setInterval(() => {
            if (!this._enabled) {
                clearInterval(this._musicInterval);
                return;
            }
            scheduleBeat();
        }, pattern.length * beatDur * 0.9 * 1000);
    },

    _playAmbienceLoop(type) {
        const loopDuration = 5;
        const ctx = this._audioCtx;

        const schedule = () => {
            if (!this._enabled) return;
            const now = ctx.currentTime;

            switch (type) {
                case 'fire': {
                    const src = this._noiseBuffer();
                    const g = ctx.createGain();
                    const f = ctx.createBiquadFilter();
                    f.type = 'lowpass';
                    f.frequency.value = 400 + Math.random() * 200;
                    f.Q.value = 0.5;
                    g.gain.setValueAtTime(0, now);
                    g.gain.linearRampToValueAtTime(0.1, now + 0.1);
                    this._crackle(g, now);
                    src.connect(f);
                    f.connect(g);
                    g.connect(this._ambienceGain);
                    src.start(now);
                    src.stop(now + loopDuration);
                    this._ambienceNodes.push(src);
                    break;
                }
                case 'wind': {
                    const src = this._noiseBuffer();
                    const g = ctx.createGain();
                    const f = ctx.createBiquadFilter();
                    f.type = 'lowpass';
                    f.frequency.setValueAtTime(200, now);
                    f.frequency.linearRampToValueAtTime(800, now + loopDuration);
                    g.gain.setValueAtTime(0, now);
                    g.gain.linearRampToValueAtTime(0.08, now + 1);
                    g.gain.linearRampToValueAtTime(0.04, now + loopDuration);
                    src.connect(f);
                    f.connect(g);
                    g.connect(this._ambienceGain);
                    src.start(now);
                    src.stop(now + loopDuration);
                    this._ambienceNodes.push(src);
                    break;
                }
                case 'rain': {
                    for (let i = 0; i < 3; i++) {
                        const src = this._noiseBuffer();
                        const g = ctx.createGain();
                        const f = ctx.createBiquadFilter();
                        f.type = 'highpass';
                        f.frequency.value = 3000 + Math.random() * 1000;
                        g.gain.setValueAtTime(0, now + i * 1.6);
                        g.gain.linearRampToValueAtTime(0.05, now + i * 1.6 + 0.2);
                        g.gain.linearRampToValueAtTime(0, now + i * 1.6 + 1.5);
                        src.connect(f);
                        f.connect(g);
                        g.connect(this._ambienceGain);
                        src.start(now + i * 1.6);
                        src.stop(now + i * 1.6 + 2);
                        this._ambienceNodes.push(src);
                    }
                    break;
                }
                case 'waves': {
                    const src = this._noiseBuffer();
                    const g = ctx.createGain();
                    const f = ctx.createBiquadFilter();
                    f.type = 'lowpass';
                    f.frequency.setValueAtTime(80, now);
                    f.frequency.linearRampToValueAtTime(500, now + 2);
                    f.frequency.linearRampToValueAtTime(80, now + 5);
                    g.gain.setValueAtTime(0, now);
                    g.gain.linearRampToValueAtTime(0.1, now + 1);
                    g.gain.linearRampToValueAtTime(0, now + 5);
                    src.connect(f);
                    f.connect(g);
                    g.connect(this._ambienceGain);
                    src.start(now);
                    src.stop(now + 5);
                    this._ambienceNodes.push(src);
                    break;
                }
                case 'dripping': {
                    for (let i = 0; i < 4; i++) {
                        const osc = ctx.createOscillator();
                        const g = ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.value = 600 + Math.random() * 400;
                        g.gain.setValueAtTime(0, now + i * 1.2);
                        g.gain.linearRampToValueAtTime(0.06, now + i * 1.2 + 0.02);
                        g.gain.exponentialRampToValueAtTime(0.001, now + i * 1.2 + 0.3);
                        osc.connect(g);
                        g.connect(this._ambienceGain);
                        osc.start(now + i * 1.2);
                        osc.stop(now + i * 1.2 + 0.3);
                        this._ambienceNodes.push(osc);
                    }
                    break;
                }
                case 'birds': {
                    for (let i = 0; i < 3; i++) {
                        const osc = ctx.createOscillator();
                        const g = ctx.createGain();
                        osc.type = 'sine';
                        const base = 2000 + Math.random() * 1500;
                        osc.frequency.setValueAtTime(base, now + i * 1.8);
                        osc.frequency.linearRampToValueAtTime(base + 400, now + i * 1.8 + 0.15);
                        osc.frequency.linearRampToValueAtTime(base, now + i * 1.8 + 0.3);
                        g.gain.setValueAtTime(0, now + i * 1.8);
                        g.gain.linearRampToValueAtTime(0.05, now + i * 1.8 + 0.02);
                        g.gain.exponentialRampToValueAtTime(0.001, now + i * 1.8 + 0.5);
                        osc.connect(g);
                        g.connect(this._ambienceGain);
                        osc.start(now + i * 1.8);
                        osc.stop(now + i * 1.8 + 0.5);
                        this._ambienceNodes.push(osc);
                    }
                    break;
                }
                case 'crowd': {
                    const src = this._noiseBuffer();
                    const g = ctx.createGain();
                    const f = ctx.createBiquadFilter();
                    f.type = 'bandpass';
                    f.frequency.value = 500 + Math.random() * 200;
                    f.Q.value = 0.5;
                    g.gain.setValueAtTime(0, now);
                    g.gain.linearRampToValueAtTime(0.03, now + 0.5);
                    g.gain.linearRampToValueAtTime(0.02, now + loopDuration);
                    src.connect(f);
                    f.connect(g);
                    g.connect(this._ambienceGain);
                    src.start(now);
                    src.stop(now + loopDuration);
                    this._ambienceNodes.push(src);
                    break;
                }
                case 'silence': default: break;
            }
        };
        schedule();
        this._ambienceInterval = setInterval(() => {
            if (!this._enabled) {
                clearInterval(this._ambienceInterval);
                return;
            }
            schedule();
        }, loopDuration * 1000);
    },

    _crackle(gain, startTime) {
        const ctx = this._audioCtx;
        for (let i = 0; i < 8; i++) {
            const t = startTime + Math.random() * 0.8;
            gain.gain.setValueAtTime(0.12, t);
            gain.gain.setValueAtTime(0, t + 0.02);
        }
    },

    _noiseBuffer() {
        const ctx = this._audioCtx;
        const len = ctx.sampleRate * 3;
        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
        const data = buf.getChannelData(0);
        for (let i = 0; i < len; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const src = ctx.createBufferSource();
        src.buffer = buf;
        src.loop = true;
        return src;
    },

    _synth(sfx) {
        const ctx = this._audioCtx;
        const now = ctx.currentTime;

        switch (sfx) {
            case 'fire': {
                const src = this._noiseBuffer();
                const g = ctx.createGain();
                const f = ctx.createBiquadFilter();
                f.type = 'lowpass';
                f.frequency.value = 300 + Math.random() * 200;
                g.gain.setValueAtTime(0, now);
                g.gain.linearRampToValueAtTime(0.2, now + 0.05);
                g.gain.setValueAtTime(0.2, now + 0.3);
                g.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                src.connect(f); f.connect(g); g.connect(this._sfxGain);
                src.start(now); src.stop(now + 1.5);
                break;
            }
            case 'rain': {
                for (let i = 0; i < 6; i++) {
                    const src = this._noiseBuffer();
                    const g = ctx.createGain();
                    const f = ctx.createBiquadFilter();
                    f.type = 'highpass';
                    f.frequency.value = 4000 + Math.random() * 2000;
                    g.gain.setValueAtTime(0, now + i * 0.08);
                    g.gain.linearRampToValueAtTime(0.03, now + i * 0.08 + 0.01);
                    g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.15);
                    src.connect(f); f.connect(g); g.connect(this._sfxGain);
                    src.start(now + i * 0.08); src.stop(now + i * 0.08 + 0.15);
                    this._ambienceNodes.push(src);
                }
                break;
            }
            case 'wind': {
                const src = this._noiseBuffer();
                const g = ctx.createGain();
                const f = ctx.createBiquadFilter();
                f.type = 'lowpass';
                f.frequency.setValueAtTime(200, now);
                f.frequency.linearRampToValueAtTime(2000, now + 2);
                g.gain.setValueAtTime(0, now);
                g.gain.linearRampToValueAtTime(0.12, now + 0.5);
                g.gain.linearRampToValueAtTime(0.08, now + 2);
                g.gain.exponentialRampToValueAtTime(0.001, now + 3);
                src.connect(f); f.connect(g); g.connect(this._sfxGain);
                src.start(now); src.stop(now + 3);
                break;
            }
            case 'footsteps': {
                for (let i = 0; i < 3; i++) {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine'; osc.frequency.value = 60 + Math.random() * 40;
                    g.gain.setValueAtTime(0, now + i * 0.4);
                    g.gain.linearRampToValueAtTime(0.25, now + i * 0.4 + 0.02);
                    g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.4 + 0.15);
                    osc.connect(g); g.connect(this._sfxGain);
                    osc.start(now + i * 0.4); osc.stop(now + i * 0.4 + 0.15);
                }
                break;
            }
            case 'sword': {
                const src = this._noiseBuffer();
                const g1 = ctx.createGain();
                const f1 = ctx.createBiquadFilter();
                f1.type = 'bandpass'; f1.frequency.value = 3000; f1.Q.value = 2;
                g1.gain.setValueAtTime(0, now);
                g1.gain.linearRampToValueAtTime(0.15, now + 0.02);
                g1.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
                src.connect(f1); f1.connect(g1); g1.connect(this._sfxGain);
                src.start(now); src.stop(now + 0.3);
                const osc = ctx.createOscillator();
                const g2 = ctx.createGain();
                osc.type = 'sine'; osc.frequency.value = 800;
                g2.gain.setValueAtTime(0, now + 0.05);
                g2.gain.linearRampToValueAtTime(0.12, now + 0.07);
                g2.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                osc.connect(g2); g2.connect(this._sfxGain);
                osc.start(now + 0.05); osc.stop(now + 0.5);
                break;
            }
            case 'magic': {
                [400, 500, 600, 800, 1000, 1200].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine'; osc.frequency.value = freq;
                    g.gain.setValueAtTime(0, now + i * 0.06);
                    g.gain.linearRampToValueAtTime(0.1, now + i * 0.06 + 0.02);
                    g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.4);
                    osc.connect(g); g.connect(this._sfxGain);
                    osc.start(now + i * 0.06); osc.stop(now + i * 0.06 + 0.4);
                });
                break;
            }
            case 'door': {
                const osc = ctx.createOscillator();
                const g = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(200, now);
                osc.frequency.linearRampToValueAtTime(80, now + 0.5);
                g.gain.setValueAtTime(0, now);
                g.gain.linearRampToValueAtTime(0.15, now + 0.05);
                g.gain.setValueAtTime(0.1, now + 0.3);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                osc.connect(g); g.connect(this._sfxGain);
                osc.start(now); osc.stop(now + 0.8);
                break;
            }
            case 'water': {
                for (let i = 0; i < 5; i++) {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine'; osc.frequency.value = 200 + Math.random() * 600;
                    g.gain.setValueAtTime(0, now + i * 0.12);
                    g.gain.linearRampToValueAtTime(0.06, now + i * 0.12 + 0.02);
                    g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.25);
                    osc.connect(g); g.connect(this._sfxGain);
                    osc.start(now + i * 0.12); osc.stop(now + i * 0.12 + 0.25);
                }
                break;
            }
            case 'monster': {
                const osc = ctx.createOscillator();
                const g = ctx.createGain();
                const f = ctx.createBiquadFilter();
                f.type = 'lowpass'; f.frequency.value = 200;
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(40, now);
                osc.frequency.linearRampToValueAtTime(80, now + 0.5);
                osc.frequency.linearRampToValueAtTime(50, now + 1);
                g.gain.setValueAtTime(0, now);
                g.gain.linearRampToValueAtTime(0.25, now + 0.05);
                g.gain.setValueAtTime(0.2, now + 0.5);
                g.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                osc.connect(f); f.connect(g); g.connect(this._sfxGain);
                osc.start(now); osc.stop(now + 1.5);
                break;
            }
            case 'bell': {
                [1, 2.76, 4.07, 6.31].forEach((h, i) => {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine'; osc.frequency.value = 440 * h;
                    g.gain.setValueAtTime(0, now);
                    g.gain.linearRampToValueAtTime(0.12 / (i + 1), now + 0.01);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 2);
                    osc.connect(g); g.connect(this._sfxGain);
                    osc.start(now); osc.stop(now + 2);
                });
                break;
            }
            case 'thunder': {
                const src = this._noiseBuffer();
                const g = ctx.createGain();
                const f = ctx.createBiquadFilter();
                f.type = 'lowpass';
                f.frequency.setValueAtTime(800, now);
                f.frequency.linearRampToValueAtTime(100, now + 0.5);
                g.gain.setValueAtTime(0, now);
                g.gain.linearRampToValueAtTime(0.35, now + 0.02);
                g.gain.exponentialRampToValueAtTime(0.25, now + 0.15);
                g.gain.exponentialRampToValueAtTime(0.001, now + 2);
                src.connect(f); f.connect(g); g.connect(this._sfxGain);
                src.start(now); src.stop(now + 2);
                break;
            }
            case 'heartbeat': {
                [0, 0.2, 0.8, 1.0].forEach((offset, i) => {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine'; osc.frequency.value = 50 + (i % 2) * 20;
                    g.gain.setValueAtTime(0, now + offset);
                    g.gain.linearRampToValueAtTime(0.3, now + offset + 0.03);
                    g.gain.exponentialRampToValueAtTime(0.001, now + offset + 0.2);
                    osc.connect(g); g.connect(this._sfxGain);
                    osc.start(now + offset); osc.stop(now + offset + 0.2);
                });
                break;
            }
            default: break;
        }
    },
};

window.AudioManager = AudioManager;
