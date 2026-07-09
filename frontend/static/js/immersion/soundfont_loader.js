const SoundFontLoader = {
    _loaded: false,
    _loading: false,
    _synth: null,
    _outputNode: null,
    _gainNode: null,

    GM_INSTRUMENTS: {
        tavern: 23, forest: 74, dungeon: 20, castle: 57, village: 74,
        city: 57, mountain: 74, library: 75, temple: 20, beach: 76,
        cave: 20, battle: 62, boss: 62, mystery: 75, epic: 57,
        sad: 75, tension: 20, adventure: 57, peaceful: 74,
    },

    async load() {
        if (this._loaded || this._loading) return this._loaded;
        this._loading = true;

        try {
            const audioCtx = window.AudioManager && window.AudioManager._audioCtx;
            if (!audioCtx) throw new Error('No AudioContext');

            const { FluidSynth } = await this._loadSynth();
            this._synth = new FluidSynth(audioCtx);

            const sf2Url = 'https://cdn.jsdelivr.net/gh/musescore/MuseScore@master/share/sound/FluidR3Mono.sf3';
            const res = await fetch(sf2Url);
            if (!res.ok) throw new Error('SF2 fetch failed');
            const sf2Buf = await res.arrayBuffer();

            await this._synth.loadSFont(new Uint8Array(sf2Buf));

            this._outputNode = this._synth.createNode();
            this._gainNode = audioCtx.createGain();
            this._gainNode.gain.value = 0.12;
            this._outputNode.connect(this._gainNode);
            this._gainNode.connect(audioCtx.destination);

            this._loaded = true;
        } catch (e) {
            // SoundFont unavailable — procedural fallback is fine
        }
        this._loading = false;
        return this._loaded;
    },

    async _loadSynth() {
        if (typeof FluidSynth !== 'undefined') return { FluidSynth };
        await new Promise((resolve, reject) => {
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/js-synthesizer@0.8.0/dist/js-synthesizer.min.js';
            s.onload = resolve;
            s.onerror = reject;
            document.head.appendChild(s);
        });
        return { FluidSynth };
    },

    isLoaded() {
        return this._loaded;
    },

    playNote(midiNote, velocity, duration) {
        if (!this._loaded || !this._synth) return;
        try {
            this._synth.noteOn(0, midiNote, velocity || 100);
            setTimeout(() => {
                try { this._synth.noteOff(0, midiNote); } catch (e) { /* ignore */ }
            }, (duration || 1) * 1000);
        } catch (e) { /* ignore */ }
    },

    playChord(scene) {
        if (!this._loaded || !this._synth) return;
        const chords = {
            tavern: [60, 64, 67], forest: [67, 65, 64, 60],
            dungeon: [48, 55, 60, 55], castle: [60, 64, 67, 62],
            battle: [55, 58, 60, 63], boss: [48, 53, 55, 53],
            temple: [67, 69, 71, 72], mystery: [67, 66, 65, 64],
        };
        const notes = chords[scene] || chords.forest;
        const prog = this.GM_INSTRUMENTS[scene] || 0;
        try {
            this._synth.programChange(0, prog);
            notes.forEach((n, i) => {
                setTimeout(() => {
                    try {
                        this._synth.noteOn(0, n, 80);
                        setTimeout(() => {
                            try { this._synth.noteOff(0, n); } catch (e) { /* ignore */ }
                        }, 2000);
                    } catch (e) { /* ignore */ }
                }, i * 400);
            });
        } catch (e) { /* ignore */ }
    },

    _freqToMIDI(freq) {
        return Math.round(12 * (Math.log(freq / 440) / Math.LN2) + 69);
    },
};

window.SoundFontLoader = SoundFontLoader;
