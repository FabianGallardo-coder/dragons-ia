const CinematicMode = {
    _initialized: false,
    _active: false,
    _overlay: null,
    _titleEl: null,
    _asciiEl: null,
    _resolveEnd: null,

    init() {
        if (this._initialized) return;
        this._buildOverlay();
        this._initialized = true;
    },

    _buildOverlay() {
        this._overlay = document.createElement('div');
        this._overlay.id = 'cinematic-overlay';
        this._overlay.style.cssText = [
            'position:fixed',
            'top:0;left:0',
            'width:100vw;height:100vh',
            'background:#000',
            'display:flex',
            'flex-direction:column',
            'align-items:center',
            'justify-content:center',
            'z-index:1000',
            'opacity:0',
            'transition:opacity 1s ease',
            'pointer-events:none',
        ].join(';');

        this._titleEl = document.createElement('h1');
        this._titleEl.style.cssText = [
            'font-family:Cinzel,serif',
            'font-size:clamp(1.5rem,5vw,3rem)',
            'color:var(--theme-border,#F59E0B)',
            'text-shadow:0 0 20px currentColor,0 0 40px currentColor',
            'margin-bottom:1rem',
            'opacity:0',
            'transform:translateY(-20px)',
            'transition:opacity 0.8s ease 0.3s,transform 0.8s ease 0.3s',
        ].join(';');

        this._asciiEl = document.createElement('pre');
        this._asciiEl.style.cssText = [
            'font-family:Courier New,Consolas,monospace',
            'font-size:clamp(0.35rem,1.2vw,0.7rem)',
            'line-height:1.1',
            'color:var(--theme-border,#F59E0B)',
            'text-shadow:0 0 4px currentColor',
            'opacity:0',
            'transform:scale(0.95)',
            'transition:opacity 0.8s ease 0.5s,transform 0.8s ease 0.5s',
            'white-space:pre',
            'text-align:center',
            'max-width:95vw',
            'max-height:70vh',
            'overflow:hidden',
        ].join(';');

        this._overlay.appendChild(this._titleEl);
        this._overlay.appendChild(this._asciiEl);
        document.body.appendChild(this._overlay);
    },

    async show(sceneData, duration) {
        if (this._active) return;
        this._active = true;
        this.init();

        const scene = sceneData.scene || 'forest';
        const title = sceneData.cinematic_title || '';

        let art;
        if (window.ASCIIManager) {
            art = window.ASCIIManager.compose(scene, Date.now());
        }
        if (!art) art = '';

        this._titleEl.textContent = title;
        this._asciiEl.textContent = art;

        if (window.AudioManager) {
            const music = sceneData.music || 'epic';
            window.AudioManager.playMusic(music);
        }

        this._overlay.style.pointerEvents = 'auto';
        this._overlay.style.opacity = '1';

        requestAnimationFrame(() => {
            this._titleEl.style.opacity = '1';
            this._titleEl.style.transform = 'translateY(0)';
            this._asciiEl.style.opacity = '1';
            this._asciiEl.style.transform = 'scale(1)';
        });

        return new Promise(resolve => {
            const wait = (duration || 4) * 1000;
            setTimeout(() => {
                this._titleEl.style.opacity = '0';
                this._titleEl.style.transform = 'translateY(-20px)';
                this._asciiEl.style.opacity = '0';
                this._asciiEl.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this._overlay.style.opacity = '0';
                    setTimeout(() => {
                        this._overlay.style.pointerEvents = 'none';
                        this._active = false;
                        resolve();
                    }, 1000);
                }, 300);
            }, wait);
        });
    },

    isActive() {
        return this._active;
    },
};

window.CinematicMode = CinematicMode;
