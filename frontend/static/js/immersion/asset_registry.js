const AssetRegistry = {
    _assets: new Map(),
    _initialized: false,

    SCENE_META: {
        tavern: { label: 'Taberna', themes: ['fantasy'], music: 'tavern', ambience: ['crowd', 'fire'] },
        cave: { label: 'Caverna', themes: ['horror', 'ruins'], music: 'dungeon', ambience: ['dripping'] },
        forest: { label: 'Bosque', themes: ['nature'], music: 'forest', ambience: ['wind', 'birds'] },
        dungeon: { label: 'Mazmorra', themes: ['horror', 'ruins'], music: 'dungeon', ambience: ['dripping', 'chains'] },
        castle: { label: 'Castillo', themes: ['royal', 'fantasy'], music: 'castle', ambience: ['crowd'] },
        village: { label: 'Aldea', themes: ['fantasy', 'nature'], music: 'village', ambience: ['crowd', 'birds'] },
        city: { label: 'Ciudad', themes: ['fantasy'], music: 'village', ambience: ['crowd', 'laughter'] },
        mountain: { label: 'Montaña', themes: ['nature'], music: 'adventure', ambience: ['wind'] },
        library: { label: 'Biblioteca', themes: ['arcane', 'holy'], music: 'mystery', ambience: ['silence'] },
        temple: { label: 'Templo', themes: ['holy', 'fantasy'], music: 'peaceful', ambience: ['silence'] },
        throne_room: { label: 'Salón del Trono', themes: ['royal'], music: 'castle', ambience: ['crowd'] },
        ship: { label: 'Barco', themes: ['nature'], music: 'adventure', ambience: ['waves'] },
        beach: { label: 'Playa', themes: ['nature'], music: 'peaceful', ambience: ['waves', 'seagulls'] },
        camp: { label: 'Campamento', themes: ['nature'], music: 'peaceful', ambience: ['fire', 'birds'] },
        graveyard: { label: 'Cementerio', themes: ['horror'], music: 'sad', ambience: ['silence'] },
        tower: { label: 'Torre', themes: ['arcane', 'fantasy'], music: 'mystery', ambience: ['wind'] },
        river: { label: 'Río', themes: ['nature'], music: 'peaceful', ambience: ['water'] },
        desert: { label: 'Desierto', themes: ['ruins', 'nature'], music: 'mystery', ambience: ['wind'] },
        market: { label: 'Mercado', themes: ['fantasy'], music: 'village', ambience: ['crowd', 'laughter'] },
        arena: { label: 'Arena', themes: ['infernal', 'ruins'], music: 'battle', ambience: ['crowd'] },
        ruins: { label: 'Ruinas', themes: ['ruins', 'horror'], music: 'mystery', ambience: ['wind', 'silence'] },
        swamp: { label: 'Pantano', themes: ['horror', 'nature'], music: 'dungeon', ambience: ['insects', 'frogs'] },
        volcano: { label: 'Volcán', themes: ['infernal'], music: 'boss', ambience: ['fire', 'crackling'] },
        ice_cave: { label: 'Cueva de Hielo', themes: ['arcane', 'horror'], music: 'mystery', ambience: ['dripping'] },
        underground: { label: 'Subterráneo', themes: ['horror', 'ruins'], music: 'dungeon', ambience: ['dripping', 'silence'] },
    },

    WEATHER_LABELS: {
        none: 'Despejado',
        rain: 'Lluvia',
        snow: 'Nieve',
        storm: 'Tormenta',
        fog: 'Niebla',
        wind: 'Viento',
        hail: 'Granizo',
        sandstorm: 'Tormenta de arena',
        clear: 'Despejado',
    },

    DANGER_LABELS: {
        peaceful: 'Pacífico',
        tense: 'Tenso',
        combat: 'Combate',
        boss: 'Jefe',
        death: 'Mortal',
    },

    THEME_LABELS: {
        fantasy: 'Fantasía',
        horror: 'Horror',
        royal: 'Imperial',
        infernal: 'Infernal',
        ruins: 'Ruinas',
        nature: 'Naturaleza',
        holy: 'Sagrado',
        arcane: 'Arcano',
        mechanical: 'Mecánico',
        underwater: 'Subacuático',
        epic: 'Épico',
    },

    TIME_LABELS: {
        dawn: 'Amanecer',
        day: 'Día',
        sunset: 'Atardecer',
        night: 'Noche',
        midnight: 'Media Noche',
    },

    LIGHT_LABELS: {
        sunlight: 'Luz Solar',
        moonlight: 'Luz Lunar',
        torch: 'Antorcha',
        magic: 'Magia',
        fireplace: 'Chimenea',
        darkness: 'Oscuridad',
        candlelight: 'Velas',
        bioluminescence: 'Bioluminiscencia',
        starlight: 'Luz Estelar',
        lava: 'Lava',
    },

    init() {
        if (this._initialized) return;
        this._initialized = true;
    },

    getSceneMeta(scene) {
        return this.SCENE_META[scene] || this.SCENE_META.forest;
    },

    getLabel(category, key) {
        const maps = {
            weather: this.WEATHER_LABELS,
            danger: this.DANGER_LABELS,
            theme: this.THEME_LABELS,
            time: this.TIME_LABELS,
            light: this.LIGHT_LABELS,
        };
        const map = maps[category];
        return map && map[key] ? map[key] : key;
    },
};

window.AssetRegistry = AssetRegistry;
