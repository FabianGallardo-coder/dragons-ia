const ThemeManager = {
    themes: {
        nature: { bg1: '#0f1f12', bg2: '#061208', border: '#22c55e', textHl: '#4ade80', glow: 'rgba(34,197,94,0.15)' },
        horror: { bg1: '#1a0505', bg2: '#0a0000', border: '#ef4444', textHl: '#f87171', glow: 'rgba(239,68,68,0.15)' },
        fantasy: { bg1: '#1a1a2e', bg2: '#16213e', border: '#F59E0B', textHl: '#FBBF24', glow: 'rgba(245,158,11,0.15)' },
        royal: { bg1: '#1e1b4b', bg2: '#0f172a', border: '#a855f7', textHl: '#c084fc', glow: 'rgba(168,85,247,0.15)' },
        epic: { bg1: '#3f1d1d', bg2: '#220909', border: '#fb923c', textHl: '#fdba74', glow: 'rgba(251,146,60,0.15)' },
        infernal: { bg1: '#450a0a', bg2: '#1a0505', border: '#dc2626', textHl: '#fca5a5', glow: 'rgba(220,38,38,0.2)' },
        ruins: { bg1: '#1f2937', bg2: '#111827', border: '#9ca3af', textHl: '#d1d5db', glow: 'rgba(156,163,175,0.1)' },
        holy: { bg1: '#172554', bg2: '#0f172a', border: '#60a5fa', textHl: '#93c5fd', glow: 'rgba(96,165,250,0.15)' },
        arcane: { bg1: '#2e1065', bg2: '#170533', border: '#c084fc', textHl: '#e879f9', glow: 'rgba(192,132,252,0.15)' },
        mechanical: { bg1: '#1e293b', bg2: '#0f172a', border: '#64748b', textHl: '#cbd5e1', glow: 'rgba(100,116,139,0.1)' },
        underwater: { bg1: '#082f49', bg2: '#041c2c', border: '#0ea5e9', textHl: '#38bdf8', glow: 'rgba(14,165,233,0.15)' },
    },

    sceneBackgrounds: {
        tavern: 'radial-gradient(ellipse at bottom, rgba(245,158,11,0.06) 0%, transparent 70%)',
        cave: 'radial-gradient(ellipse at top, rgba(100,116,139,0.08) 0%, transparent 70%)',
        forest: 'radial-gradient(ellipse at center, rgba(34,197,94,0.05) 0%, transparent 70%)',
        dungeon: 'radial-gradient(ellipse at top, rgba(239,68,68,0.06) 0%, transparent 70%)',
        castle: 'radial-gradient(ellipse at bottom, rgba(168,85,247,0.06) 0%, transparent 70%)',
        village: 'radial-gradient(ellipse at bottom, rgba(245,158,11,0.04) 0%, transparent 70%)',
        city: 'radial-gradient(ellipse at bottom, rgba(251,191,36,0.05) 0%, transparent 70%)',
        mountain: 'radial-gradient(ellipse at center, rgba(148,163,184,0.04) 0%, transparent 70%)',
        beach: 'radial-gradient(ellipse at bottom, rgba(56,189,248,0.05) 0%, transparent 70%)',
        desert: 'radial-gradient(ellipse at center, rgba(251,191,36,0.05) 0%, transparent 70%)',
        temple: 'radial-gradient(ellipse at bottom, rgba(250,204,21,0.05) 0%, transparent 70%)',
        library: 'radial-gradient(ellipse at center, rgba(192,132,252,0.04) 0%, transparent 70%)',
        graveyard: 'radial-gradient(ellipse at top, rgba(156,163,175,0.05) 0%, transparent 70%)',
        river: 'radial-gradient(ellipse at bottom, rgba(56,189,248,0.04) 0%, transparent 70%)',
        swamp: 'radial-gradient(ellipse at center, rgba(34,197,94,0.04) 0%, transparent 70%)',
        volcano: 'radial-gradient(ellipse at top, rgba(220,38,38,0.08) 0%, transparent 70%)',
        ice_cave: 'radial-gradient(ellipse at center, rgba(147,197,253,0.05) 0%, transparent 70%)',
        arena: 'radial-gradient(ellipse at center, rgba(239,68,68,0.06) 0%, transparent 70%)',
    },

    dangerColors: {
        peaceful: null,
        tense: '#eab308',
        combat: '#ef4444',
        boss: '#b91c1c',
        death: '#000000',
    },

    apply(sceneData) {
        const root = document.documentElement;
        const theme = this.themes[sceneData.theme] || this.themes.fantasy;

        root.style.setProperty('--theme-bg1', theme.bg1);
        root.style.setProperty('--theme-bg2', theme.bg2);
        root.style.setProperty('--theme-text-hl', theme.textHl);
        root.style.setProperty('--theme-glow', theme.glow);

        let borderColor = theme.border;
        if (sceneData.danger !== 'peaceful' && this.dangerColors[sceneData.danger]) {
            borderColor = this.dangerColors[sceneData.danger];
        }
        root.style.setProperty('--theme-border', borderColor);

        const scene = sceneData.scene || 'forest';
        const bgRadial = this.sceneBackgrounds[scene] || 'none';
        root.style.setProperty('--theme-scene-bg', bgRadial);

        let brightness = 1.0;
        if (sceneData.time === 'night' || sceneData.time === 'midnight') {
            brightness = 0.8;
        }
        if (sceneData.light === 'darkness') {
            brightness = 0.5;
        } else if (sceneData.light === 'sunlight' || sceneData.light === 'magic') {
            brightness = 1.1;
        }
        root.style.setProperty('--theme-brightness', brightness);

        this._applyDangerGlow(sceneData.danger, borderColor);
    },

    _applyDangerGlow(danger, color) {
        const container = document.getElementById('ascii-art-container');
        if (!container) return;

        if (danger === 'combat' || danger === 'boss') {
            container.style.boxShadow = `0 0 20px ${color}40, 0 0 40px ${color}20`;
            container.style.borderColor = color;
        } else if (danger === 'death') {
            container.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
            container.style.borderColor = '#374151';
        } else {
            container.style.boxShadow = 'none';
            container.style.borderColor = 'rgba(245, 158, 11, 0.15)';
        }
    },
};

window.ThemeManager = ThemeManager;
