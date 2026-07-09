const AnimationManager = {
    _initialized: false,
    _currentWeather: null,
    _particleCount: 0,
    _frameId: null,
    _container: null,
    _activeParticles: [],

    PARTICLE_CONFIGS: {
        rain: { count: 40, symbol: '|', color: 'rgba(148, 163, 184, 0.4)', speed: 2, size: 1 },
        snow: { count: 25, symbol: '*', color: 'rgba(255, 255, 255, 0.6)', speed: 0.8, size: 2 },
        fog: { count: 15, symbol: '.', color: 'rgba(200, 200, 200, 0.15)', speed: 0.3, size: 3 },
        embers: { count: 12, symbol: '.', color: 'rgba(251, 191, 36, 0.7)', speed: 0.5, size: 2 },
        dust: { count: 20, symbol: '.', color: 'rgba(180, 160, 120, 0.2)', speed: 0.4, size: 1 },
        leaves: { count: 8, symbol: '~', color: 'rgba(74, 222, 128, 0.3)', speed: 0.6, size: 2 },
        sparks: { count: 10, symbol: '*', color: 'rgba(250, 204, 21, 0.8)', speed: 1.5, size: 1 },
        bubbles: { count: 10, symbol: 'o', color: 'rgba(147, 197, 253, 0.3)', speed: 0.5, size: 1 },
        none: { count: 0 },
    },

    WEATHER_MAP: {
        rain: 'rain',
        storm: 'rain',
        snow: 'snow',
        fog: 'fog',
        wind: 'dust',
        sandstorm: 'dust',
        clear: 'none',
        none: 'none',
    },

    SFX_MAP: {
        none: 'none',
        fire: 'embers',
        magic: 'sparks',
        water: 'bubbles',
    },

    init() {
        if (this._initialized) return;

        this._container = document.createElement('div');
        this._container.id = 'particle-container';
        this._container.style.cssText =
            'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;z-index:0;';

        const gameLog = document.getElementById('game-log');
        if (gameLog) {
            gameLog.style.position = 'relative';
            gameLog.style.zIndex = '1';
            gameLog.parentNode.insertBefore(this._container, gameLog);
        } else {
            document.body.appendChild(this._container);
        }

        this._initialized = true;
    },

    apply(sceneData) {
        if (!this._initialized) this.init();

        const weather = sceneData.weather || 'none';
        const sfx = sceneData.sfx || 'none';

        let particleType = this.WEATHER_MAP[weather] || 'none';
        if (particleType === 'none') {
            particleType = this.SFX_MAP[sfx] || 'none';
        }

        if (particleType === this._currentWeather) return;
        this._currentWeather = particleType;

        this._clear();
        if (particleType === 'none') return;

        const config = this.PARTICLE_CONFIGS[particleType];
        if (!config || config.count === 0) return;

        this._spawn(config);
    },

    _spawn(config) {
        for (let i = 0; i < config.count; i++) {
            const el = document.createElement('div');
            el.textContent = config.symbol;
            el.style.cssText = [
                'position:absolute',
                `left:${Math.random() * 100}%`,
                `top:${Math.random() * -20}%`,
                `color:${config.color}`,
                `font-size:${config.size * 10}px`,
                'font-family:monospace',
                'pointer-events:none',
                'user-select:none',
                `opacity:${Math.random() * 0.5 + 0.3}`,
                'will-change:transform',
            ].join(';');

            this._container.appendChild(el);

            const duration = (3 + Math.random() * 4) / config.speed;
            const xDrift = (Math.random() - 0.5) * 100;
            const rotation = Math.random() * 360;

            el.animate([
                { transform: 'translateY(0) rotate(0deg)', opacity: parseFloat(el.style.opacity) },
                { transform: `translate(${xDrift}px, 110vh) rotate(${rotation}deg)`, opacity: 0 },
            ], {
                duration: duration * 1000,
                iterations: 1,
                easing: 'linear',
                fill: 'forwards',
            }).onfinish = () => el.remove();

            this._activeParticles.push(el);
        }

        setTimeout(() => this._cleanup(), (5 / config.speed) * 1000);
    },

    _clear() {
        this._activeParticles.forEach(el => {
            if (el && el.parentNode) el.remove();
        });
        this._activeParticles = [];
        if (this._container) {
            this._container.innerHTML = '';
        }
    },

    _cleanup() {
        this._activeParticles = this._activeParticles.filter(el => el && el.parentNode);
    },
};

window.AnimationManager = AnimationManager;
