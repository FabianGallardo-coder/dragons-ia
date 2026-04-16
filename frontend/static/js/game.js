/**
 * Dragons & IA — game.js
 * Lógica principal del juego: acciones, renderizado de historia, dados.
 */

let currentDiceResult = null;
let isProcessing = false;
let diceUsedThisTurn = false;

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
    } catch (err) {
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
        addDMMessage(response.narrative);

        // Actualizar UI
        updateHP(response.character_hp, response.character_hp_max);
        document.getElementById('turn-display').textContent = `Turno ${response.turn_count}`;

        // Verificar muerte del personaje
        if (!response.character_alive) {
            addSystemMessage('💀 Tu personaje ha caído. La aventura ha terminado.');
            document.getElementById('action-form').style.display = 'none';
        }

    } catch (err) {
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
    if (diceUsedThisTurn) {
        return; // ya tiró este turno
    }
    diceUsedThisTurn = true;

    const result = Math.floor(Math.random() * sides) + 1;
    currentDiceResult = result;
    const display = document.getElementById('dice-result');
    display.textContent = `🎲 d${sides}: ${result}`;

    // Deshabilitar botones de dados hasta el próximo turno
    _enableDiceButtons(false);
    document.getElementById('dice-used-msg').classList.remove('hidden');

    // Animación breve
    display.classList.add('scale-125');
    setTimeout(() => display.classList.remove('scale-125'), 200);
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
 * Agrega un mensaje del DM al log.
 */
function addDMMessage(text) {
    const container = document.getElementById('narrative-container');
    const div = document.createElement('div');
    div.className = 'message-dm';
    div.textContent = text;
    container.appendChild(div);
    scrollToBottom();
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
 * Actualiza la barra de HP.
 */
function updateHP(current, max) {
    const display = document.getElementById('hp-display');
    display.textContent = `❤️ ${current}/${max}`;
    if (current <= max * 0.25) {
        display.className = 'text-red-400 font-bold';
    } else if (current <= max * 0.5) {
        display.className = 'text-yellow-400 font-bold';
    } else {
        display.className = 'text-emerald-400 font-bold';
    }
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
function exitGame() {
    if (confirm('¿Seguro que querés salir? La partida se guarda automáticamente.')) {
        location.href = '/';
    }
}
