const GLSLFX = {
    _initialized: false,
    _canvas: null,
    _gl: null,
    _program: null,
    _animId: null,
    _currentEffect: null,
    _startTime: 0,

    SHADERS: {
        fire: {
            vertex: [
                'attribute vec2 aPos;',
                'void main() { gl_Position = vec4(aPos, 0.0, 1.0); }',
            ].join('\n'),
            fragment: [
                'precision highp float;',
                'uniform float uTime;',
                'uniform vec2 uRes;',
                'void main() {',
                '  vec2 uv = gl_FragCoord.xy / uRes;',
                '  float t = uTime * 2.0;',
                '  float r = 0.5 + 0.5 * sin(uv.x * 10.0 + t) * sin(uv.y * 8.0 - t * 1.3);',
                '  float g = 0.3 + 0.3 * sin(uv.x * 7.0 - t * 0.7) * sin(uv.y * 6.0 + t);',
                '  float b = 0.1 + 0.1 * sin(uv.x * 5.0 + t * 0.5) * sin(uv.y * 4.0 - t * 0.3);',
                '  float alpha = 1.0 - uv.y;',
                '  gl_FragColor = vec4(r, g, b, alpha * 0.3);',
                '}',
            ].join('\n'),
        },
        water: {
            vertex: [
                'attribute vec2 aPos;',
                'void main() { gl_Position = vec4(aPos, 0.0, 1.0); }',
            ].join('\n'),
            fragment: [
                'precision highp float;',
                'uniform float uTime;',
                'uniform vec2 uRes;',
                'void main() {',
                '  vec2 uv = gl_FragCoord.xy / uRes;',
                '  float t = uTime * 0.5;',
                '  float wave = sin(uv.x * 15.0 + t) * 0.5 + 0.5;',
                '  float wave2 = sin(uv.y * 10.0 - t * 0.7) * 0.5 + 0.5;',
                '  float r = 0.0 + 0.1 * wave;',
                '  float g = 0.3 + 0.3 * wave2;',
                '  float b = 0.5 + 0.4 * wave;',
                '  float alpha = 0.15 + 0.1 * sin(uv.x * 8.0 + uv.y * 6.0 + t);',
                '  gl_FragColor = vec4(r, g, b, alpha);',
                '}',
            ].join('\n'),
        },
        fog: {
            vertex: [
                'attribute vec2 aPos;',
                'void main() { gl_Position = vec4(aPos, 0.0, 1.0); }',
            ].join('\n'),
            fragment: [
                'precision highp float;',
                'uniform float uTime;',
                'uniform vec2 uRes;',
                'void main() {',
                '  vec2 uv = gl_FragCoord.xy / uRes;',
                '  float t = uTime * 0.2;',
                '  float f1 = sin(uv.x * 8.0 + uv.y * 6.0 + t) * 0.5 + 0.5;',
                '  float f2 = sin(uv.x * 12.0 - uv.y * 10.0 + t * 1.3) * 0.5 + 0.5;',
                '  float alpha = (f1 * 0.3 + f2 * 0.2) * (1.0 - uv.y * 0.5);',
                '  gl_FragColor = vec4(0.6, 0.6, 0.65, alpha * 0.25);',
                '}',
            ].join('\n'),
        },
        magic: {
            vertex: [
                'attribute vec2 aPos;',
                'void main() { gl_Position = vec4(aPos, 0.0, 1.0); }',
            ].join('\n'),
            fragment: [
                'precision highp float;',
                'uniform float uTime;',
                'uniform vec2 uRes;',
                'void main() {',
                '  vec2 uv = gl_FragCoord.xy / uRes;',
                '  vec2 c = uv - 0.5;',
                '  float t = uTime * 1.5;',
                '  float dist = length(c);',
                '  float angle = atan(c.y, c.x);',
                '  float spiral = sin(dist * 15.0 - t * 3.0 + angle * 3.0) * 0.5 + 0.5;',
                '  float glow = exp(-dist * 4.0);',
                '  float r = 0.6 * spiral + 0.4 * glow;',
                '  float g = 0.3 * spiral + 0.6 * glow;',
                '  float b = 0.9 * spiral + 0.8 * glow;',
                '  float alpha = (spiral * 0.3 + glow * 0.8) * 0.3;',
                '  gl_FragColor = vec4(r, g, b, alpha);',
                '}',
            ].join('\n'),
        },
    },

    EFFECT_SCENE_MAP: {
        fire: ['volcano', 'infernal'],
        water: ['beach', 'river', 'underwater', 'swamp'],
        fog: ['fog', 'mystery', 'ruins', 'graveyard', 'cave'],
        magic: ['arcane', 'library', 'temple', 'magic'],
    },

    init() {
        if (this._initialized) return;
        this._canvas = document.createElement('canvas');
        this._canvas.id = 'glsl-canvas';
        this._canvas.style.cssText = [
            'position:fixed',
            'top:0;left:0',
            'width:100vw;height:100vh',
            'pointer-events:none',
            'z-index:0',
            'opacity:0',
            'transition:opacity 2s ease',
        ].join(';');

        const gameLog = document.getElementById('game-log');
        if (gameLog) {
            gameLog.parentNode.insertBefore(this._canvas, gameLog);
        } else {
            document.body.appendChild(this._canvas);
        }

        this._initialized = true;
    },

    apply(sceneData) {
        if (!this._initialized) this.init();
        const scene = sceneData.scene || 'forest';
        const theme = sceneData.theme || 'nature';

        let effect = null;
        for (const [fx, scenes] of Object.entries(this.EFFECT_SCENE_MAP)) {
            if (scenes.includes(scene) || scenes.includes(theme)) {
                effect = fx;
                break;
            }
        }

        if (effect === this._currentEffect) return;
        this._currentEffect = effect;

        if (!effect) {
            this.hide();
            return;
        }

        this._start(effect);
    },

    _start(effect) {
        const shader = this.SHADERS[effect];
        if (!shader) return;

        this._ensureSize();
        this._gl = this._canvas.getContext('webgl', { premultipliedAlpha: false, alpha: true });
        if (!this._gl) return;

        const gl = this._gl;

        const vs = gl.createShader(gl.VERTEX_SHADER);
        gl.shaderSource(vs, shader.vertex);
        gl.compileShader(vs);

        const fs = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(fs, shader.fragment);
        gl.compileShader(fs);

        this._program = gl.createProgram();
        gl.attachShader(this._program, vs);
        gl.attachShader(this._program, fs);
        gl.linkProgram(this._program);
        gl.useProgram(this._program);

        const positions = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
        const aPos = gl.getAttribLocation(this._program, 'aPos');
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

        this._uTime = gl.getUniformLocation(this._program, 'uTime');
        this._uRes = gl.getUniformLocation(this._program, 'uRes');

        this._startTime = performance.now();
        this._canvas.style.opacity = '1';
        this._render();
    },

    _render() {
        if (!this._gl || !this._currentEffect) return;
        const gl = this._gl;
        const now = (performance.now() - this._startTime) / 1000;

        gl.uniform1f(this._uTime, now);
        gl.uniform2f(this._uRes, this._canvas.width, this._canvas.height);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        gl.finish();

        this._animId = requestAnimationFrame(() => this._render());
    },

    _ensureSize() {
        this._canvas.width = window.innerWidth * (window.devicePixelRatio || 1);
        this._canvas.height = window.innerHeight * (window.devicePixelRatio || 1);
        this._canvas.style.width = '100vw';
        this._canvas.style.height = '100vh';
    },

    hide() {
        this._currentEffect = null;
        this._canvas.style.opacity = '0';
        if (this._animId) {
            cancelAnimationFrame(this._animId);
            this._animId = null;
        }
        if (this._gl) {
            const gl = this._gl;
            const ext = gl.getExtension('WEBGL_lose_context');
            if (ext) ext.loseContext();
            this._gl = null;
        }
    },
};

window.GLSLFX = GLSLFX;
