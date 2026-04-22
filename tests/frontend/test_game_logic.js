/**
 * Tests de lógica pura del frontend — game.js
 *
 * Ejecutar con: node tests/frontend/test_game_logic.js
 *
 * No requiere dependencias externas (solo Node.js stdlib).
 * Prueba funciones puras extraídas del código de juego:
 * - WORLD_FONTS: mapeo completo de mundos a fuentes
 * - Lógica de detección crítico/fumble del dado
 * - Máquina de estados de setAIStatus
 * - Lógica de updateXP (cálculo de nivel)
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

// ── Reproducir constantes y lógica de game.js ────────────────────

const WORLD_FONTS = {
    fantasia: {
        name: 'Cinzel',
        url: 'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap',
        css: "'Cinzel', serif",
    },
    ciencia_ficcion: {
        name: 'Orbitron',
        url: 'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap',
        css: "'Orbitron', monospace",
    },
    isekai: {
        name: 'Philosopher',
        url: 'https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400&display=swap',
        css: "'Philosopher', serif",
    },
    fantasia_oscura: {
        name: 'Crimson Text',
        url: 'https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap',
        css: "'Crimson Text', serif",
    },
};

// Lógica de clasificación del resultado del dado
function classifyRoll(sides, result) {
    if (sides === 20 && result === 20) return 'critical';
    if (sides === 20 && result === 1)  return 'fumble';
    return 'normal';
}

// Lógica de cálculo de nivel (copiada de game.js)
function calculateLevel(xp) {
    return Math.floor(xp / 100) + 1;
}

function xpInLevel(xp) {
    return xp % 100;
}

// Máquina de estados de setAIStatus
const AI_STATES = {
    idle:     { dot: 'bg-gray-600',                    text: 'IA',        cls: 'text-gray-600' },
    thinking: { dot: 'bg-yellow-400 animate-pulse',    text: 'Pensando…', cls: 'text-yellow-400' },
    ok:       { dot: 'bg-emerald-500',                 text: 'Conectada', cls: 'text-emerald-400' },
    error:    { dot: 'bg-red-500',                     text: 'Error',     cls: 'text-red-400' },
};

// ── Suite: WORLD_FONTS ────────────────────────────────────────────

console.log('\nWORLD_FONTS');

test('tiene los 4 mundos del juego', () => {
    const worlds = ['fantasia', 'ciencia_ficcion', 'isekai', 'fantasia_oscura'];
    worlds.forEach(w => assert.ok(WORLD_FONTS[w], `Falta mundo: ${w}`));
});

test('cada fuente tiene name, url y css', () => {
    Object.entries(WORLD_FONTS).forEach(([world, font]) => {
        assert.ok(font.name,  `${world}: falta name`);
        assert.ok(font.url,   `${world}: falta url`);
        assert.ok(font.css,   `${world}: falta css`);
    });
});

test('todas las URLs apuntan a Google Fonts', () => {
    Object.entries(WORLD_FONTS).forEach(([world, font]) => {
        assert.ok(
            font.url.startsWith('https://fonts.googleapis.com'),
            `${world}: URL no apunta a Google Fonts`
        );
    });
});

test('ciencia_ficcion usa fuente monospace', () => {
    assert.ok(WORLD_FONTS.ciencia_ficcion.css.includes('monospace'));
});

test('fantasia_oscura no tiene la misma fuente que fantasia', () => {
    assert.notStrictEqual(
        WORLD_FONTS.fantasia_oscura.name,
        WORLD_FONTS.fantasia.name
    );
});

test('mundo inexistente no tiene entrada en WORLD_FONTS', () => {
    assert.strictEqual(WORLD_FONTS['western'], undefined);
});

// ── Suite: Lógica de dados ────────────────────────────────────────

console.log('\nLógica de dados');

test('d20=20 es crítico', () => {
    assert.strictEqual(classifyRoll(20, 20), 'critical');
});

test('d20=1 es fumble', () => {
    assert.strictEqual(classifyRoll(20, 1), 'fumble');
});

test('d20=10 es normal', () => {
    assert.strictEqual(classifyRoll(20, 10), 'normal');
});

test('d6=6 no es crítico (solo d20 tiene crítico)', () => {
    assert.strictEqual(classifyRoll(6, 6), 'normal');
});

test('d6=1 no es fumble (solo d20 tiene fumble)', () => {
    assert.strictEqual(classifyRoll(6, 1), 'normal');
});

test('d20=19 no es crítico (requiere exactamente 20)', () => {
    assert.strictEqual(classifyRoll(20, 19), 'normal');
});

test('d20=2 no es fumble (requiere exactamente 1)', () => {
    assert.strictEqual(classifyRoll(20, 2), 'normal');
});

// ── Suite: Cálculo de nivel / XP ─────────────────────────────────

console.log('\nCálculo de nivel/XP');

test('0 XP = nivel 1', () => {
    assert.strictEqual(calculateLevel(0), 1);
});

test('99 XP = nivel 1 (no ha subido)', () => {
    assert.strictEqual(calculateLevel(99), 1);
});

test('100 XP = nivel 2', () => {
    assert.strictEqual(calculateLevel(100), 2);
});

test('250 XP = nivel 3', () => {
    assert.strictEqual(calculateLevel(250), 3);
});

test('XP dentro del nivel actual = resto mod 100', () => {
    assert.strictEqual(xpInLevel(150), 50);
});

test('XP exacto en umbral = 0 dentro del nivel', () => {
    assert.strictEqual(xpInLevel(200), 0);
});

// ── Suite: Máquina de estados IA ──────────────────────────────────

console.log('\nEstados de IA');

test('tiene los 4 estados definidos', () => {
    ['idle', 'thinking', 'ok', 'error'].forEach(s => {
        assert.ok(AI_STATES[s], `Falta estado: ${s}`);
    });
});

test('estado "thinking" tiene animate-pulse', () => {
    assert.ok(AI_STATES.thinking.dot.includes('animate-pulse'));
});

test('estado "ok" tiene color verde (emerald)', () => {
    assert.ok(AI_STATES.ok.dot.includes('emerald'));
});

test('estado "error" tiene color rojo', () => {
    assert.ok(AI_STATES.error.dot.includes('red'));
});

test('estado "idle" texto es "IA"', () => {
    assert.strictEqual(AI_STATES.idle.text, 'IA');
});

test('estado "thinking" texto indica actividad', () => {
    assert.ok(AI_STATES.thinking.text.length > 0);
    assert.notStrictEqual(AI_STATES.thinking.text, 'IA');
});

test('cada estado tiene dot, text y cls', () => {
    Object.entries(AI_STATES).forEach(([name, state]) => {
        assert.ok(state.dot,  `${name}: falta dot`);
        assert.ok(state.text, `${name}: falta text`);
        assert.ok(state.cls,  `${name}: falta cls`);
    });
});

// ── Resumen ───────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(45)}`);
const total = passed + failed;
console.log(`Resultado: ${passed}/${total} tests pasaron`);
if (failed > 0) {
    console.error(`${failed} test(s) FALLARON`);
    process.exit(1);
} else {
    console.log('Todos los tests pasaron ✓');
}
