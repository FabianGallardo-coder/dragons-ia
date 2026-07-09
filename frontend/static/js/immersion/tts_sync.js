const TTSSync = {
    _initialized: false,
    _lastScene: null,
    _announcements: {
        combat: '¡Cuidado! Combate inminente.',
        boss: '¡Un jefe se aproxima! Preparaos.',
        death: 'La muerte acecha en la oscuridad...',
        victory: '¡Victoria! La batalla ha sido ganada.',
        scene: 'Un nuevo lugar se revela ante vosotros.',
        rest: 'Tomad un merecido descanso.',
    },

    init() {
        if (this._initialized) return;
        this._initialized = true;
    },

    apply(sceneData) {
        if (!window.TTS || !window.TTS.enabled) return;

        const danger = sceneData.danger || 'peaceful';
        const scene = sceneData.scene || 'forest';
        if (scene === this._lastScene) return;
        this._lastScene = scene;

        const msg = this._announcements[danger] || this._announcements.scene;
        const sceneName = window.AssetRegistry
            ? (window.AssetRegistry.getSceneMeta(scene).label || scene)
            : scene;

        window.TTS.speak(`${sceneName}. ${msg}`);
    },
};

window.TTSSync = TTSSync;
