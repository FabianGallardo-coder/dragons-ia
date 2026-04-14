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
        statFields.forEach(stat => {
            // 4d6 drop lowest
            const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
            rolls.sort((a, b) => a - b);
            const value = rolls[1] + rolls[2] + rolls[3];
            document.getElementById(`stat-${stat}`).value = value;
        });
    });

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

        // Guardar temporalmente y pasar a confirmación
        localStorage.setItem('dia_pending_character', JSON.stringify(charData));
        location.href = '/confirm.html';
    });
});
