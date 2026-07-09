const ImmersionEngine = {
    _initialized: false,
    _currentSceneData: null,

    init() {
        if (this._initialized) return;
        this._initialized = true;
    },

    update(responseData) {
        if (!this._initialized) this.init();

        const sceneData = window.SceneAnalyzer.analyze(responseData);

        if (this._isSameScene(sceneData) && responseData.character_alive) {
            return;
        }

        this._currentSceneData = sceneData;

        if (window.AssetRegistry) {
            window.AssetRegistry.init();
        }

        if (window.GLSLFX) {
            window.GLSLFX.apply(sceneData);
        }

        if (window.ThemeManager) {
            window.ThemeManager.apply(sceneData);
        }

        if (window.ASCIIManager) {
            window.ASCIIManager.apply(sceneData);
        }

        if (window.AnimationManager) {
            window.AnimationManager.apply(sceneData);
        }

        if (window.AudioManager) {
            window.AudioManager.apply(sceneData);
        }

        if (window.TTSSync) {
            window.TTSSync.apply(sceneData);
        }
    },

    async showCinematic(sceneData, duration) {
        if (window.CinematicMode) {
            await window.CinematicMode.show(sceneData, duration);
        }
    },

    _isSameScene(newScene) {
        if (!this._currentSceneData) return false;
        const keys = ['scene', 'weather', 'time', 'danger', 'theme'];
        return keys.every(k => this._currentSceneData[k] === newScene[k]);
    },
};

window.ImmersionEngine = ImmersionEngine;
