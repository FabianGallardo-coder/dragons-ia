/**
 * Dragons & IA — character.js
 * Lógica del wizard de creación de personaje.
 */

document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const world = localStorage.getItem('dia_selected_world');
    if (!world) {
        location.href = '/world.html';
        return;
    }

    const WORLD_NAMES = {
        fantasia: 'Fantasía Medieval',
        ciencia_ficcion: 'Ciencia Ficción',
        isekai: 'Isekai',
        fantasia_oscura: 'Fantasía Oscura',
    };

    document.getElementById('world-label').textContent =
        `Mundo: ${WORLD_NAMES[world] || world}`;

    // Botón de tirar stats
    document.getElementById('btn-roll-stats').addEventListener('click', () => {
        const statFields = [
            'fuerza', 'destreza', 'constitucion',
            'inteligencia', 'sabiduria', 'carisma'
        ];

        let total;
        let values;
        let attempts = 0;
        const MAX_TOTAL = 80; // Límite D&D 5e para evitar stats absurdos

        // Tirar hasta obtener un set legítimo (total ≤ 80)
        do {
            values = {};
            total = 0;
            statFields.forEach(stat => {
                // 4d6 drop lowest
                const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
                rolls.sort((a, b) => a - b);
                const value = rolls[1] + rolls[2] + rolls[3]; // min 3, max 18
                values[stat] = value;
                total += value;
            });
            attempts++;
        } while (total > MAX_TOTAL && attempts < 20);

        // Aplicar valores
        statFields.forEach(stat => {
            document.getElementById(`stat-${stat}`).value = values[stat];
        });

        // Mostrar total
        _updateStatsTotal();
    });

    // Actualizar total cuando cambian las stats manualmente
    const statInputs = document.querySelectorAll('#stats-grid input[type=number]');
    statInputs.forEach(input => {
        input.addEventListener('change', _updateStatsTotal);
        input.addEventListener('input', _updateStatsTotal);
    });

    function _updateStatsTotal() {
        const statFields = ['fuerza', 'destreza', 'constitucion', 'inteligencia', 'sabiduria', 'carisma'];
        let total = 0;
        statFields.forEach(stat => {
            total += parseInt(document.getElementById(`stat-${stat}`).value) || 0;
        });

        let existing = document.getElementById('stats-total');
        if (!existing) {
            existing = document.createElement('p');
            existing.id = 'stats-total';
            existing.className = 'text-xs mt-2 text-center';
            document.getElementById('stats-grid').after(existing);
        }

        if (total > 80) {
            existing.textContent = `Total: ${total}/80 ⚠️ Demasiado alto — reducí stats o tirá de nuevo`;
            existing.className = 'text-xs mt-2 text-center text-red-400';
        } else if (total > 72) {
            existing.textContent = `Total: ${total}/80 — Stats muy buenos 🔥`;
            existing.className = 'text-xs mt-2 text-center text-amber-400';
        } else {
            existing.textContent = `Total: ${total}/80 — Stats estándar`;
            existing.className = 'text-xs mt-2 text-center text-gray-500';
        }
    }

    // Enviar formulario
    document.getElementById('character-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error-msg');
        errorDiv.classList.add('hidden');

        const charData = {
            name: document.getElementById('char-name').value.trim(),
            world: world,
            race: document.getElementById('char-race').value,
            gender: document.getElementById('char-gender').value,
            character_class: document.getElementById('char-class').value,
            unique_object: document.getElementById('char-object').value.trim(),
            stats: {
                fuerza: parseInt(document.getElementById('stat-fuerza').value),
                destreza: parseInt(document.getElementById('stat-destreza').value),
                constitucion: parseInt(document.getElementById('stat-constitucion').value),
                inteligencia: parseInt(document.getElementById('stat-inteligencia').value),
                sabiduria: parseInt(document.getElementById('stat-sabiduria').value),
                carisma: parseInt(document.getElementById('stat-carisma').value),
            },
        };

        // Validaciones básicas
        if (!charData.name || charData.name.length < 2) {
            errorDiv.textContent = 'El nombre debe tener al menos 2 caracteres.';
            errorDiv.classList.remove('hidden');
            return;
        }

        if (!charData.unique_object || charData.unique_object.length < 2) {
            errorDiv.textContent = 'Describe el objeto único de tu personaje.';
            errorDiv.classList.remove('hidden');
            return;
        }

        // Validar stats D&D 5e
        const statValues = Object.values(charData.stats);
        const statTotal = statValues.reduce((a, b) => a + b, 0);
        const maxStat = Math.max(...statValues);
        const minStat = Math.min(...statValues);

        if (minStat < 3 || maxStat > 18) {
            errorDiv.textContent = 'Cada stat debe estar entre 3 y 18.';
            errorDiv.classList.remove('hidden');
            return;
        }

        if (statTotal > 80) {
            errorDiv.textContent = `Total de stats (${statTotal}) supera el máximo de 80. Tirá de nuevo o reducí valores.`;
            errorDiv.classList.remove('hidden');
            return;
        }

        // Guardar temporalmente y pasar a confirmación
        localStorage.setItem('dia_pending_character', JSON.stringify(charData));
        location.href = '/confirm.html';
    });
});
