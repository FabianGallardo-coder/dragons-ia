/**
 * Dragons & IA — game.js
 * Lógica principal del juego: acciones, renderizado de historia, dados.
 */

let currentDiceResult = null;
let isProcessing = false;
let diceUsedThisTurn = false;

// ── Fuentes por tipo de aventura ──────────────────────────────
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

function applyWorldFont(world) {
    const font = WORLD_FONTS[world];
    if (!font) return;
    const existing = document.querySelector(`link[href="${font.url}"]`);
    if (existing) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = font.url;
    document.head.appendChild(link);
    const container = document.getElementById('narrative-container');
    if (container) container.style.fontFamily = font.css;
}

document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const saveId = localStorage.getItem('dia_active_save');
    if (!saveId) {
        location.href = '/';
        return;
    }

    // Cargar partida existente
    try {
        const save = await apiGet(`/game/saves/${saveId}`);
        const charId = save.character_id;
        const character = await apiGet(`/characters/${charId}`);

        applyWorldFont(character.world);

        // Verificar si la partida sigue activa
        if (!save.is_active) {
            addSystemMessage('💀 Esta partida ha terminado. Tu personaje ha caído.');
            document.getElementById('action-form').style.display = 'none';
        }

        // Header info
        document.getElementById('char-info').textContent =
            `${character.name} — ${character.race} ${character.character_class} Nv.${character.level}`;
        updateHP(character.hp_current, character.hp_max);
        document.getElementById('turn-display').textContent = `Turno ${save.turn_count}`;

        // Renderizar historial
        renderHistory(save.history);
        scrollToBottom();
        setAIStatus('ok');

        if (window.ImmersionEngine) {
            try {
                window.ImmersionEngine.update({ narrative: 'Nueva aventura', character_alive: true, scene_data: { scene: 'tavern' } });
            } catch (e) { console.warn('ImmersionEngine init error:', e); }
        }
    } catch (err) {
        setAIStatus('error');
        addSystemMessage('Error al cargar la partida: ' + err.message);
    }

    // Formulario de acción
    document.getElementById('action-form').addEventListener('submit', handleAction);
});

/**
 * Maneja el envío de una acción al DM.
 */
async function handleAction(e) {
    e.preventDefault();

    if (isProcessing) return;

    const input = document.getElementById('action-input');
    const action = input.value.trim();
    if (!action) return;

    const saveId = localStorage.getItem('dia_active_save');
    if (!saveId) return;

    isProcessing = true;
    input.value = '';
    showLoading(true);
    setAIStatus('thinking');

    // Mostrar mensaje del jugador
    addPlayerMessage(action, currentDiceResult);

    try {
        const config = getGameConfig();
        // Validar que el modelo sea un ID real (contiene / o empieza con claude)
        const model = config.model && (config.model.includes('/') || config.model.startsWith('claude'))
            ? config.model : null;
        const response = await apiPost('/game/action', {
            save_id: saveId,
            action: action,
            dice_result: currentDiceResult,
            ai_model: model,
            api_key: config.apiKey || null,
        });

        // Mostrar respuesta del DM
        addDMMessage(response.narrative, response.narrative_tts);

        // Actualizar UI
        updateHP(response.character_hp, response.character_hp_max);
        updateXP(response.character_xp || 0);
        document.getElementById('turn-display').textContent = `Turno ${response.turn_count}`;

        setAIStatus('ok');

        if (window.ImmersionEngine) {
            try {
                window.ImmersionEngine.update(response);
            } catch (e) { console.warn('ImmersionEngine update error:', e); }
        }

        // Verificar muerte del personaje
        if (!response.character_alive) {
            addSystemMessage('💀 Tu personaje ha caído. La aventura ha terminado.');
            document.getElementById('action-form').style.display = 'none';
        }

    } catch (err) {
        setAIStatus('error');
        addSystemMessage('❌ Error: ' + err.message);
    } finally {
        currentDiceResult = null;
        diceUsedThisTurn = false;
        _enableDiceButtons(true);
        document.getElementById('dice-result').textContent = '';
        document.getElementById('dice-used-msg').classList.add('hidden');
        isProcessing = false;
        showLoading(false);
        scrollToBottom();
    }
}

/**
 * Tira un dado del tipo indicado. Solo 1 tiro por turno.
 */
function rollDice(sides) {
    if (diceUsedThisTurn) return;
    diceUsedThisTurn = true;

    const result = Math.floor(Math.random() * sides) + 1;
    currentDiceResult = result;

    const isCritical = sides === 20 && result === 20;
    const isFumble   = sides === 20 && result === 1;

    const display = document.getElementById('dice-result');
    // Resetear clases previas
    display.className = 'font-bold ml-2 self-center transition-all';

    if (isCritical) {
        display.textContent = `🎲 d20: 20 ⚡ ¡CRÍTICO!`;
        display.classList.add('text-yellow-300', 'dice-critical');
        showToast('⚡ ¡GOLPE CRÍTICO! Nat 20', 'green');
    } else if (isFumble) {
        display.textContent = `🎲 d20: 1 💀 FALLO TOTAL`;
        display.classList.add('text-red-400');
        showToast('💀 ¡Fallo Total! Nat 1', 'red');
    } else {
        display.textContent = `🎲 d${sides}: ${result}`;
        display.classList.add('text-amber-400');
        showToast(`🎲 Tiraste d${sides}: ${result}`, 'amber');
    }

    _enableDiceButtons(false);
    document.getElementById('dice-used-msg').classList.remove('hidden');

    display.classList.add('dice-rolling');
    setTimeout(() => display.classList.remove('dice-rolling'), 400);
}

/**
 * Habilita o deshabilita los botones de dados.
 */
function _enableDiceButtons(enabled) {
    document.querySelectorAll('#dice-bar .dice-btn').forEach(btn => {
        btn.disabled = !enabled;
        btn.classList.toggle('opacity-40', !enabled);
        btn.classList.toggle('cursor-not-allowed', !enabled);
    });
}

/**
 * Renderiza el historial completo de la partida.
 */
function renderHistory(history) {
    const container = document.getElementById('narrative-container');
    container.innerHTML = '';
    history.forEach(entry => {
        if (entry.role === 'assistant') {
            addDMMessage(entry.content);
        } else if (entry.role === 'user') {
            addPlayerMessage(entry.content, entry.dice_roll);
        }
    });
}

/**
 * Agrega un mensaje del DM al log con formato de párrafos.
 */
function addDMMessage(text, ttsText) {
    const container = document.getElementById('narrative-container');
    const div = document.createElement('div');
    div.className = 'message-dm';

    // Encabezado del DM
    const hdr = document.createElement('div');
    hdr.className = 'message-dm-header';
    hdr.textContent = '🧙 Dungeon Master';
    div.appendChild(hdr);

    // Cuerpo con párrafos separados
    const body = document.createElement('div');
    body.className = 'message-dm-body';
    const paragraphs = text.split(/\n+/).filter(p => p.trim());
    (paragraphs.length ? paragraphs : [text]).forEach(p => {
        const pEl = document.createElement('p');
        pEl.textContent = p.trim();
        body.appendChild(pEl);
    });
    div.appendChild(body);

    container.appendChild(div);
    scrollToBottom();

    if (typeof TTS !== 'undefined') TTS.speak(ttsText || text);
}

/**
 * Agrega un mensaje del jugador al log.
 */
function addPlayerMessage(text, diceResult) {
    const container = document.getElementById('narrative-container');

    if (diceResult != null) {
        const diceDiv = document.createElement('div');
        diceDiv.className = 'message-dice';
        diceDiv.textContent = `🎲 Resultado del dado: ${diceResult}`;
        container.appendChild(diceDiv);
    }

    const div = document.createElement('div');
    div.className = 'message-player';
    div.textContent = `> ${text}`;
    container.appendChild(div);
    scrollToBottom();
}

/**
 * Muestra un mensaje de sistema (errores, info).
 */
function addSystemMessage(text) {
    const container = document.getElementById('narrative-container');
    const div = document.createElement('div');
    div.className = 'text-center text-gray-500 italic py-2 text-sm';
    div.textContent = text;
    container.appendChild(div);
    scrollToBottom();
}

/**
 * Actualiza la barra de HP con visual.
 */
function updateHP(current, max) {
    const display = document.getElementById('hp-display');
    display.textContent = `❤️ ${current}/${max}`;

    const percent = max > 0 ? (current / max) * 100 : 0;
    const bar = document.getElementById('hp-bar');
    if (bar) {
        bar.style.width = `${percent}%`;
        if (percent <= 25) {
            bar.className = 'hp-bar-fill bg-red-500';
            display.className = 'text-red-400 font-bold text-xs';
        } else if (percent <= 50) {
            bar.className = 'hp-bar-fill bg-yellow-500';
            display.className = 'text-yellow-400 font-bold text-xs';
        } else {
            bar.className = 'hp-bar-fill bg-emerald-500';
            display.className = 'text-emerald-400 font-bold text-xs';
        }
    }
}

/**
 * Actualiza la barra de XP.
 */
function updateXP(xp) {
    const display = document.getElementById('xp-display');
    if (!display) return;
    // XP para subir de nivel: nivel * 100 (simplificado)
    const level = Math.floor(xp / 100) + 1;
    const xpInLevel = xp % 100;
    display.textContent = `⭐ Nv.${level} — XP ${xpInLevel}/100`;

    const bar = document.getElementById('xp-bar');
    if (bar) {
        bar.style.width = `${xpInLevel}%`;
    }
}

/**
 * Actualiza el indicador de estado de la IA en el header.
 * @param {'idle'|'thinking'|'ok'|'error'} status
 */
function setAIStatus(status) {
    const dot   = document.getElementById('ai-dot');
    const label = document.getElementById('ai-label');
    if (!dot || !label) return;
    const states = {
        idle:     { dot: 'bg-gray-600',                          text: 'IA',         cls: 'text-gray-600' },
        thinking: { dot: 'bg-yellow-400 animate-pulse',          text: 'Pensando…',  cls: 'text-yellow-400' },
        ok:       { dot: 'bg-emerald-500',                       text: 'Conectada',  cls: 'text-emerald-400' },
        error:    { dot: 'bg-red-500',                           text: 'Error',      cls: 'text-red-400' },
    };
    const s = states[status] || states.idle;
    dot.className   = `w-2 h-2 rounded-full inline-block ${s.dot}`;
    label.className = `text-xs ${s.cls}`;
    label.textContent = s.text;
}

/**
 * Muestra una notificación toast temporal.
 */
function showToast(message, color = 'gray') {
    const colors = {
        amber: 'bg-amber-800 text-amber-100 border border-amber-600',
        red: 'bg-red-900 text-red-100 border border-red-600',
        green: 'bg-emerald-900 text-emerald-100 border border-emerald-600',
        gray: 'bg-gray-800 text-gray-100 border border-gray-600',
    };
    const toast = document.createElement('div');
    toast.className = `toast ${colors[color] || colors.gray}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

/**
 * Muestra/oculta el indicador de carga.
 */
function showLoading(show) {
    document.getElementById('loading-indicator').classList.toggle('hidden', !show);
}

/**
 * Scroll al final del log.
 */
function scrollToBottom() {
    const main = document.getElementById('game-log');
    setTimeout(() => main.scrollTop = main.scrollHeight, 50);
}

/**
 * Envía una acción rápida predefinida.
 */
function quickAction(action) {
    const input = document.getElementById('action-input');
    input.value = action;
    document.getElementById('action-form').dispatchEvent(new Event('submit'));
}

/**
 * Guarda manualmente la partida actual.
 */
async function saveGame() {
    const saveId = localStorage.getItem('dia_active_save');
    if (!saveId) return;
    try {
        await apiPost(`/game/saves/${saveId}/save`, {});
        addSystemMessage('💾 Partida guardada correctamente.');
    } catch (err) {
        addSystemMessage('❌ Error al guardar: ' + err.message);
    }
}



/**
 * Sale del juego y vuelve al inicio.
 */
async function exitGame() {
    if (confirm('¿Seguro que querés salir?')) {
        await saveGame();
        location.href = '/';
    }
}
