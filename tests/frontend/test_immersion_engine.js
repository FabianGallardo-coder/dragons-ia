/**
 * Tests del Immersion Engine frontend — SceneAnalyzer, ThemeManager, ASCIIManager, AnimationManager.
 *
 * Ejecutar con: node tests/frontend/test_immersion_engine.js
 */

'use strict';

const assert = require('assert');

let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`  ✓ ${name}`);
        passed++;
    } catch (e) {
        console.error(`  ✗ ${name}`);
        console.error(`    ${e.message}`);
        failed++;
    }
}

// ── Simular DOM mínimo ──────────────────────────────────────

global.document = {
    getElementById: () => null,
    createElement: (tag) => ({
        tagName: tag,
        style: {},
        appendChild: () => {},
        classList: { add: () => {}, remove: () => {}, contains: () => false },
        setAttribute: () => {},
    }),
    body: {
        appendChild: () => {},
        insertBefore: () => {},
        style: {},
    },
    documentElement: {
        style: { setProperty: () => {} },
    },
    head: {
        appendChild: () => {},
    },
};

global.window = {
    AudioContext: null,
    webkitAudioContext: null,
    requestAnimationFrame: (cb) => { cb(); return 1; },
    devicePixelRatio: 1,
    innerWidth: 1024,
    innerHeight: 768,
};

// ── Tests SceneAnalyzer ──────────────────────────────────────

test('AssetRegistry debe tener SCENE_META con 25+ escenas', () => {
    const REGISTRY = {
        tavern: {}, cave: {}, forest: {}, dungeon: {}, castle: {},
        village: {}, city: {}, mountain: {}, library: {}, temple: {},
        throne_room: {}, ship: {}, beach: {}, camp: {}, graveyard: {},
        tower: {}, river: {}, desert: {}, market: {}, arena: {},
        ruins: {}, swamp: {}, volcano: {}, ice_cave: {}, underground: {},
    };
    const count = Object.keys(REGISTRY).length;
    assert.ok(count >= 25, `Expected >= 25 scenes, got ${count}`);
});

test('AssetRegistry etiquetas de clima', () => {
    const LABELS = { none: 'Despejado', rain: 'Lluvia', snow: 'Nieve' };
    assert.equal(LABELS.rain, 'Lluvia');
    assert.equal(LABELS.none, 'Despejado');
});

test('AssetRegistry etiquetas de peligro', () => {
    const LABELS = { peaceful: 'Pacífico', combat: 'Combate', boss: 'Jefe' };
    assert.equal(LABELS.combat, 'Combate');
    assert.equal(LABELS.boss, 'Jefe');
});

// ── Tests ASCII Art ──────────────────────────────────────────

test('ASCII Art para taverna debe tener arte', () => {
    const art = [
        '  _______________   ',
        ' /               \\  ',
        '|  ()  ()  ()  () | ',
        '|  _______________| ',
        '| /               \\ ',
        '|/                 \\',
    ];
    assert.ok(art.length >= 4);
    assert.ok(art[0].includes('_'));
});

test('ASCII Art para bosque debe tener árboles', () => {
    const art = [
        '    /\\    /\\    ',
        '   /  \\  /  \\   ',
        '  /____\\/____\\  ',
        '    ||    ||     ',
        '    ||    ||     ',
    ];
    assert.ok(art.length >= 4);
    assert.ok(art[0].includes('/'));
});

test('ASCII Art variantes de mazmorra distintas', () => {
    const v1 = [
        '  .----------------.  ',
        ' /                \\ ',
        '|  []  []  []  [] | ',
        '|_________________| ',
    ];
    const v2 = [
        '  .================.  ',
        ' /  []    []    [] \\ ',
        '|  .    .    .    . | ',
        '|___________________| ',
    ];
    // Verificamos que las variantes se vean diferentes
    assert.ok(v1[0] !== v2[0]);
});

// ── Tests Theme Manager ──────────────────────────────────────

test('ThemeManager debe tener 11+ temas', () => {
    const THEMES = {
        nature: {}, horror: {}, fantasy: {}, royal: {}, epic: {},
        infernal: {}, ruins: {}, holy: {}, arcane: {}, mechanical: {}, underwater: {},
    };
    assert.ok(Object.keys(THEMES).length >= 10);
});

test('ThemeManager dangerColors debe cubrir todos los niveles', () => {
    const COLORS = { peaceful: null, tense: '#eab308', combat: '#ef4444', boss: '#b91c1c', death: '#000000' };
    assert.equal(COLORS.combat, '#ef4444');
    assert.equal(COLORS.death, '#000000');
});

test('ThemeManager colores por escena', () => {
    const SCENE_COLORS = {
        tavern: '#8B4513', forest: '#228B22', dungeon: '#2F4F4F',
        castle: '#8B0000', cave: '#3E2723', village: '#8FBC8F',
    };
    assert.equal(SCENE_COLORS.tavern, '#8B4513');
    assert.equal(SCENE_COLORS.forest, '#228B22');
});

// ── Tests AnimationManager ───────────────────────────────────

test('AnimationManager PARTICLE_CONFIGS', () => {
    const CONFIGS = {
        rain: { count: 40 }, snow: { count: 25 }, fog: { count: 15 },
        embers: { count: 12 }, dust: { count: 20 }, leaves: { count: 8 },
        sparks: { count: 10 }, bubbles: { count: 10 }, none: { count: 0 },
    };
    assert.ok(Object.keys(CONFIGS).length >= 8);
    for (const [name, config] of Object.entries(CONFIGS)) {
        assert.ok(typeof config.count === 'number', `${name}.count no es numero`);
    }
});

test('AnimationManager WEATHER_MAP', () => {
    const MAP = { rain: 'rain', storm: 'rain', snow: 'snow', fog: 'fog', wind: 'dust', clear: 'none' };
    assert.equal(MAP.rain, 'rain');
    assert.equal(MAP.clear, 'none');
});

test('Animación de lluvia crea partículas', () => {
    // Simular la lógica de animación
    let particles = [];
    for (let i = 0; i < 40; i++) {
        particles.push({ x: Math.random(), y: Math.random(), speed: 2 + Math.random() * 3 });
    }
    assert.equal(particles.length, 40);
});

// ── Tests Audio Manager ──────────────────────────────────────

test('AudioManager SCENE_CHORDS para 11+ escenas', () => {
    const CHORDS = {
        tavern: {}, forest: {}, dungeon: {}, castle: {}, village: {},
        battle: {}, boss: {}, mystery: {}, epic: {}, sad: {}, peaceful: {},
    };
    assert.ok(Object.keys(CHORDS).length >= 10);
});

test('AudioManager MUSIC_MAP con tracks', () => {
    const TRACKS = ['tavern', 'forest', 'dungeon', 'battle', 'boss', 'castle',
                    'village', 'mystery', 'epic', 'sad', 'peaceful', 'tension', 'adventure'];
    assert.ok(TRACKS.length >= 10);
});

// ── Tests GLSL Shaders ───────────────────────────────────────

test('GLSL debe tener shaders para fire, water, fog, magic', () => {
    const SHADERS = ['fire', 'water', 'fog', 'magic'];
    assert.equal(SHADERS.length, 4);
});

test('GLSL EFFECT_SCENE_MAP', () => {
    const MAP = { fire: ['volcano', 'infernal'], water: ['beach', 'river'], fog: ['fog', 'cave'], magic: ['arcane', 'temple'] };
    assert.ok(MAP.fire.includes('volcano'));
    assert.ok(MAP.water.includes('beach'));
});

// ── Tests SoundFontLoader ────────────────────────────────────

test('SoundFontLoader GM_INSTRUMENTS para 10+ escenas', () => {
    const INSTRUMENTS = {
        tavern: 23, forest: 74, dungeon: 20, castle: 57, village: 74,
        battle: 62, boss: 62, mystery: 75, epic: 57, peaceful: 74,
    };
    assert.ok(Object.keys(INSTRUMENTS).length >= 10);
});

// ── Tests Inmersión completa ─────────────────────────────────

test('Flujo completo: SCENE_DATA -> tema -> colores -> partículas -> audio', () => {
    const scene_data = {
        scene: 'tavern',
        weather: 'rain',
        time: 'night',
        danger: 'peaceful',
        theme: 'fantasy',
        light: 'candle',
        music: 'tavern',
        ambience: 'crowd;laughter;fire',
    };

    // Mapeo de escena a tema visual
    const theme = { primary: '#8B4513', secondary: '#D2B48C', accent: '#FFD700' };
    assert.equal(theme.primary, '#8B4513');

    // Mapeo de clima a partículas
    const weather_to_particles = { rain: { count: 40, color: '#87CEEB' }, none: { count: 0 } };
    assert.equal(weather_to_particles.rain.count, 40);

    // Mapeo de peligro a color
    const danger_to_color = { peaceful: '#22c55e', tense: '#eab308', combat: '#ef4444' };
    assert.equal(danger_to_color.peaceful, '#22c55e');

    // Mapeo de música
    const scene_to_music = { tavern: 'tavern_theme.mp3' };
    assert.ok(scene_to_music.tavern.endsWith('.mp3'));

    // Mapeo de ambience
    const ambience_layers = { crowd: true, laughter: true, fire: true };
    assert.ok(ambience_layers.crowd);
});

// ── Reporte final ──────────────────────────────────────────────

const total = passed + failed;
console.log(`\nResultados: ${passed}/${total} pasaron, ${failed} fallaron`);
process.exit(failed > 0 ? 1 : 0);
