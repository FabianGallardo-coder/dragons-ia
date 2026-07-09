/**
 * Dragons & IA — Immersion Engine: Scene Analyzer
 * 
 * Analiza los datos de escena recibidos del backend. Si falta información,
 * usa expresiones regulares como fallback para deducir la escena a partir
 * del texto narrativo.
 */

const SceneAnalyzer = {
    // Escenas por defecto si falla el análisis
    DEFAULT_SCENE: 'forest',
    DEFAULT_THEME: 'nature',
    DEFAULT_DANGER: 'peaceful',

    /**
     * Procesa la respuesta de la API y extrae o deduce los datos de escena.
     * @param {Object} responseData - La respuesta completa de la API (/game/action o /game/new)
     * @returns {Object} Datos de escena garantizados
     */
    analyze(responseData) {
        const narrative = responseData.narrative || '';
        
        // 1. Usar SCENE_DATA si el backend lo proveyó
        if (responseData.scene_data && typeof responseData.scene_data === 'object') {
            return this._normalize(responseData.scene_data);
        }

        // 2. Fallback: Deducir por regex si el modelo omitió SCENE_DATA
        return this._fallbackAnalyze(narrative);
    },

    /**
     * Normaliza los datos de escena asegurando que tengan valores válidos.
     */
    _normalize(data) {
        return {
            scene: data.scene || this.DEFAULT_SCENE,
            weather: data.weather || 'none',
            time: data.time || 'day',
            danger: data.danger || this.DEFAULT_DANGER,
            theme: data.theme || this.DEFAULT_THEME,
            light: data.light || 'sunlight',
            music: data.music || 'adventure',
            ambience: Array.isArray(data.ambience) ? data.ambience : (data.ambience ? [data.ambience.split(';').map(s=>s.trim())] : []),
            sfx: data.sfx || 'none',
            ascii: data.ascii || data.scene || this.DEFAULT_SCENE
        };
    },

    /**
     * Analiza el texto narrativo para deducir el contexto.
     */
    _fallbackAnalyze(text) {
        const lower = text.toLowerCase();
        
        const data = {
            scene: this.DEFAULT_SCENE,
            danger: this.DEFAULT_DANGER,
            theme: this.DEFAULT_THEME,
            time: 'day',
            weather: 'none'
        };

        // Peligro / Combate
        if (/mueres|has caído|agonía|te desplomas|tinieblas|oscuridad eterna/.test(lower)) {
            data.danger = 'death';
            data.theme = 'horror';
        } else if (/atacas?|golpeas?|combate|te ataca|embistes|contraatacas|luchas|espadazos?/.test(lower)) {
            data.danger = 'combat';
        } else if (/jefe|dragón|titán|demonio mayor|rey/.test(lower)) {
            data.danger = 'boss';
            data.theme = 'epic';
        }

        // Escena / Tema
        if (/taberna|posada|cerveza|mesero/.test(lower)) {
            data.scene = 'tavern';
            data.theme = 'fantasy';
        } else if (/cueva|caverna|gruta|subterráneo/.test(lower)) {
            data.scene = 'cave';
            data.theme = 'horror';
            data.light = 'torch';
        } else if (/castillo|palacio|fortaleza|rey|reina/.test(lower)) {
            data.scene = 'castle';
            data.theme = 'royal';
        } else if (/bosque|árboles|naturaleza|fauna/.test(lower)) {
            data.scene = 'forest';
            data.theme = 'nature';
        } else if (/ciudad|pueblo|villa|calles|mercado/.test(lower)) {
            data.scene = 'city';
            data.theme = 'fantasy';
        }

        // Tiempo
        if (/noche|oscuridad|luna|estrellas/.test(lower)) {
            data.time = 'night';
            if (data.light === 'sunlight') data.light = 'moonlight';
        }

        return this._normalize(data);
    }
};

// Exportar globalmente
window.SceneAnalyzer = SceneAnalyzer;
