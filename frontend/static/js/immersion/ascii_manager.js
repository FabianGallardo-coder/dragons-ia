const ASCIIManager = {
    _initialized: false,
    _currentScene: null,
    _seed: Date.now(),
    _prng: null,

    _BG: {
        tavern: [
            '        ___________         ',
            '      /\'         \'\\       ',
            '     /  _  _  _    \\      ',
            '    |  ( ) ( ) ( )  |     ',
            '    |   _   _   _   |     ',
            '    |  |_| |_| |_|  |     ',
            '    |    _______    |     ',
            '   /|   |       |   |\\    ',
            '  / |   | [] [] |   | \\   ',
            ' /  |   |_______|   |  \\  ',
        ],
        cave: [
            '      .-\"\"\"\"\"-.         ',
            '     /         \\        ',
            '    /  _     _  \\       ',
            '   |  |_|   |_|  |      ',
            '   |    _____     |     ',
            '   |   |_ _ _|   |     ',
            '    \\   \\___/   /      ',
            '     \\         /       ',
            '      \'--...--\'        ',
        ],
        forest: [
            '        ,,     ,,        ',
            '       /  \\   /  \\      ',
            '      / /\\ \\ / /\\ \\     ',
            '     / /__\\/ /__\\ \\    ',
            '    |  _    _    _  |    ',
            '    | |_|  |_|  |_| |    ',
            '    |   ___________ |    ',
            '    \\_/           \\_/    ',
            '      |   |   |   |      ',
            '     /|   |   |   |\\     ',
            '    /_|   |   |   |_\\    ',
        ],
        dungeon: [
            '    .-\"\"\"\"\"\"\"\"\"-.      ',
            '   /  _  _  _  _  \\     ',
            '  |  |_||_||_||_|  |    ',
            '  |   ___  ___  __  |    ',
            '  |  |___||___||__| |    ',
            '  |  _  _  _  _     |    ',
            '  | |_||_||_||_|    |    ',
            '   \\               /     ',
            '    \'-.._______..-\'      ',
        ],
        castle: [
            '       ___             ',
            '      /\\ \\\\    /\\      ',
            '     /  \\_\\\\  /  \\     ',
            '    / /\\__\\\\/ /\\ \\    ',
            '   / /__\\\\/\\/ /__\\ \\   ',
            '  /________\\/______\\  ',
            '  |  _   __   _   |   ',
            '  | |_| |  | |_|  |   ',
            '  |______|__|______|   ',
            '   |  |      |  |     ',
            '   |__|      |__|     ',
        ],
        village: [
            '      /\\     /\\       ',
            '     /  \\   /  \\      ',
            '    / /\\ \\ / /\\ \\     ',
            '   / /__\\/ /__\\ \\    ',
            '  |  ___   ___  |     ',
            '  | |_|_| |_|_| |     ',
            '  |   ___   ___  |    ',
            '  \\_|_|_|_|_|_|_|/    ',
            '    |  |   |  |      ',
            '    |__|   |__|      ',
        ],
        mountain: [
            '        /\\            ',
            '       /  \\    /\\     ',
            '      / /\\ \\  /  \\    ',
            '     / /__\\ \\/ /\\ \\   ',
            '    /_______\\/ /__\\ \\  ',
            '    \\_______\\______/  ',
            '     \\      /\\       ',
            '      \\    /  \\      ',
            '       \\  / /\\ \\     ',
            '        \\/ /__\\ \\    ',
        ],
        beach: [
            '   ~  ~ ~  ~ ~ ~ ~    ',
            '  ~ ~ ~  ~ ~ ~ ~ ~   ',
            ' ~  ~  ~  ~  ~  ~ ~  ',
            '~ ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
            ' ~ ~ /\\ ~ ~ ~ ~ ~   ',
            '  ~ /  \\  ~ ~ ~ ~    ',
            ' ~ / /\\ \\ ~ ~ ~ ~   ',
            '~ ~/_/__\\_\\~ ~ ~ ~  ',
            ' ~~~~~~~~~~~~~~~ ~   ',
            '  ~~~~~~~~~~~~~~~    ',
        ],
        desert: [
            '  ~ ~ ~ ~ ~ ~ ~ ~    ',
            ' ~ ~ ~ ~ ~ ~ ~ ~ ~   ',
            '~ ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
            ' ~ ~ ~ ~ ~ ~ ~ ~ ~   ',
            '  ~ ~ ~ ~ ~ ~ ~ ~    ',
            '   ~ ~ ~ ~ ~ ~ ~     ',
            '  ~ ~ ~ ~ ~ ~ ~ ~    ',
            ' ~ ~ ~ ~ ~ ~ ~ ~ ~   ',
            '~ ~ ~ ~ ~ ~ ~ ~ ~ ~  ',
            ' ~ ~ ~ ~ ~ ~ ~ ~ ~   ',
        ],
        temple: [
            '        /\\           ',
            '       /  \\          ',
            '      / /\\ \\         ',
            '     / /__\\ \\        ',
            '    /_______\\        ',
            '    |  ___  |        ',
            '    | |   | |        ',
            '    | | o | |        ',
            '    | |___| |        ',
            '    |_______|        ',
            '     |_____|         ',
        ],
        library: [
            '    .-\"\"\"\"\"\"-.       ',
            '   /  _  _  _  \\     ',
            '  |  || || || |  |   ',
            '  |  || || || |  |   ',
            '  |  || || || |  |   ',
            '  |  |_||_||_|  |   ',
            '   \\           /    ',
            '    \'-..___..-\'     ',
            '       |   |        ',
            '      /|   |\\       ',
        ],
    },

    _FEATURES: [
        // 0: tree
        [
            '    /\\    ',
            '   /  \\   ',
            '  / /\\ \\  ',
            ' / /__\\ \\ ',
            '/_______\\',
        ],
        // 1: pine
        [
            '    /\\     ',
            '   //\\\\    ',
            '  ///\\\\\\   ',
            ' /////\\\\\\  ',
            '   |||     ',
        ],
        // 2: rock
        [
            '  __   ',
            ' /  \\_ ',
            '|__  _|',
            '   \\/  ',
        ],
        // 3: window
        [
            ' [ ] ',
            ' | | ',
            ' [ ] ',
        ],
        // 4: torch
        [
            '  ,  ',
            '  |  ',
            '  |  ',
        ],
        // 5: pillar
        [
            ' |||| ',
            ' |||| ',
            ' |||| ',
            ' |||| ',
        ],
        // 6: fountain
        [
            '   o   ',
            '  \\|/  ',
            '  / \\  ',
        ],
        // 7: bookshelf
        [
            ' [=] [=] ',
            ' |======|',
            ' [===]   ',
            ' |======|',
        ],
        // 8: anvil
        [
            '  __  ',
            ' /  \\ ',
            '| __ |',
        ],
        // 9: chest
        [
            ' .---. ',
            ' | | | ',
            ' \'-\'-\\\' ',
        ],
        // 10: campfire
        [
            '  ,\'\'\',  ',
            ' ,\'   \', ',
            '  \'   \'  ',
        ],
        // 11: bush
        [
            ' ,,, ',
            '((()))',
            ' ,,.,,',
        ],
        // 12: ladder
        [
            ' |-| ',
            ' |-| ',
            ' |-| ',
            ' |-| ',
        ],
        // 13: statue
        [
            '  .\'.  ',
            ' /|o|\\ ',
            ' / | \\ ',
            '  / \\  ',
        ],
        // 14: barrel
        [
            ' .-\'. ',
            ' | | |',
            ' \'-\'- ',
        ],
    ],

    _CREATURES: [
        // 0: knight (friendly NPC)
        [
            '  O   ',
            ' /|\\  ',
            ' / \\  ',
        ],
        // 1: goblin (enemy)
        [
            '  o.  ',
            ' /|\\\' ',
            ' / \\  ',
        ],
        // 2: wizard
        [
            '  O,  ',
            ' /|\\  ',
            ' / \\  ',
            ' /    ',
        ],
        // 3: dragon (mini)
        [
            '  /\\   ',
            ' /\\/\\  ',
            ' |  |  ',
            ' \\__/  ',
        ],
        // 4: ghost
        [
            ' .\\\'. ',
            ' | o |',
            ' \'._.\'',
        ],
        // 5: merchant
        [
            '  O   ',
            ' /|\\  ',
            ' /|\\  ',
        ],
        // 6: dog
        [
            ' .-. ',
            ' | | ',
            ' \\_/ ',
        ],
        // 7: skeleton
        [
            ' .o.  ',
            ' /|\\  ',
            ' / \\  ',
        ],
        // 8: bat
        [
            ' /\\/\\ ',
            ' \\  / ',
            '  \\/  ',
        ],
        // 9: snake
        [
            ' ~  ',
            '~~  ',
            ' ~\\ ',
        ],
    ],

    _DECORATIONS: [
        // 0: stars
        [
            ' *   ',
            '   * ',
            ' *   ',
            '   * ',
        ],
        // 1: spiderweb
        [
            ' /\\ ',
            '/\\/\\',
            ' \\/ ',
        ],
        // 2: candle
        [
            ' i  ',
            ' |  ',
            ' |  ',
            ' |  ',
        ],
        // 3: mushrooms
        [
            ' . . ',
            ' \'\'\' ',
        ],
        // 4: vines
        [
            ' ,, ',
            '((  ',
            '  ))',
            ' ,( ',
        ],
    ],

    init() {
        if (this._initialized) return;
        this._seed = Date.now();
        this._prng = this._mulberry32(this._seed);
        this._initialized = true;
    },

    _mulberry32(seed) {
        return function() {
            let t = seed += 0x6D2B79F5;
            t = Math.imul(t ^ t >>> 15, t | 1);
            t ^= t + Math.imul(t ^ t >>> 7, t | 61);
            return ((t ^ t >>> 14) >>> 0) / 4294967296;
        };
    },

    _rand(max) {
        if (!this._prng) this._prng = this._mulberry32(this._seed);
        return Math.floor(this._prng() * max);
    },

    _randFloat() {
        if (!this._prng) this._prng = this._mulberry32(this._seed);
        return this._prng();
    },

    _grid(str) {
        return str.split('\n').map(r => r.split(''));
    },

    _unparse(grid) {
        return grid.map(r => r.join('')).join('\n');
    },

    _overlay(base, layer, offsetRow = 0, offsetCol = 0) {
        for (let r = 0; r < layer.length; r++) {
            const targetR = offsetRow + r;
            if (targetR < 0 || targetR >= base.length) continue;
            for (let c = 0; c < layer[r].length; c++) {
                const targetC = offsetCol + c;
                if (targetC < 0 || targetC >= base[targetR].length) continue;
                if (layer[r][c] !== ' ') {
                    base[targetR][targetC] = layer[r][c];
                }
            }
        }
    },

    compose(scene, seed) {
        if (seed !== undefined) {
            this._seed = seed;
            this._prng = this._mulberry32(this._seed);
        } else {
            this._seed = Date.now();
            this._prng = this._mulberry32(this._seed);
        }

        const bgKey = this._BG[scene] ? scene : 'forest';
        const bg = this._BG[bgKey];
        if (!bg) return '';

        const grid = bg.map(r => r.split(''));

        const numFeatures = 1 + this._rand(3);
        for (let i = 0; i < numFeatures; i++) {
            const fi = this._rand(this._FEATURES.length);
            const feature = this._FEATURES[fi];
            const maxRow = grid.length - feature.length;
            const maxCol = grid[0].length - feature[0].length;
            if (maxRow > 0 && maxCol > 0) {
                const row = this._rand(maxRow);
                const col = this._rand(maxCol);
                this._overlay(grid, feature.map(r => r.split('')), row, col);
            }
        }

        if (this._randFloat() < 0.6) {
            const ci = this._rand(this._CREATURES.length);
            const creature = this._CREATURES[ci];
            const maxRow = grid.length - creature.length;
            const maxCol = grid[0].length - creature[0].length;
            if (maxRow > 0 && maxCol > 0) {
                const row = grid.length - creature.length;
                const col = this._rand(maxCol);
                this._overlay(grid, creature.map(r => r.split('')), row, col);
            }
        }

        if (this._randFloat() < 0.4) {
            const di = this._rand(this._DECORATIONS.length);
            const deco = this._DECORATIONS[di];
            const maxRow = grid.length - deco.length;
            const maxCol = grid[0].length - deco[0].length;
            if (maxRow > 0 && maxCol > 0) {
                const row = this._rand(maxRow);
                const col = this._rand(maxCol);
                this._overlay(grid, deco.map(r => r.split('')), row, col);
            }
        }

        return this._unparse(grid);
    },

    getSceneArt(scene, variant) {
        const seed = variant ? (variant * 9301 + 49297) % 233280 : Date.now();
        return this.compose(scene, seed);
    },

    getTitle(event, world) {
        const titles = {
            new_game: 'NUEVA AVENTURA',
            battle: 'COMBATE',
            victory: 'VICTORIA',
            death: 'HAS MUERTO',
            scene: 'CAMBIO DE ESCENA',
            rest: 'DESCANSO',
            boss: 'JEFE FINAL',
        };
        return titles[event] || event.toUpperCase();
    },

    apply(sceneData) {
        const scene = sceneData.scene || 'forest';
        const asciiHint = sceneData.ascii || scene;

        let variant = 0;
        if (scene === this._currentScene) {
            this._seed = (this._seed * 9301 + 49297) % 233280;
            variant = this._seed;
        } else {
            this._currentScene = scene;
            variant = 0;
        }

        const art = this.getSceneArt(asciiHint, variant);
        this._render(art, sceneData);
    },

    _render(art, sceneData) {
        const container = document.getElementById('ascii-art-container');
        const display = document.getElementById('ascii-art-display');
        if (!container || !display) return;

        const dangerColor = sceneData.danger === 'combat' || sceneData.danger === 'boss'
            ? '#ef4444' : sceneData.danger === 'death' ? '#6b7280' : '#F59E0B';

        container.classList.remove('danger-combat', 'danger-boss');
        if (sceneData.danger === 'combat') container.classList.add('danger-combat');
        if (sceneData.danger === 'boss') container.classList.add('danger-boss');

        const fadeOut = () => {
            return new Promise(resolve => {
                container.style.opacity = '0';
                container.addEventListener('transitionend', resolve, { once: true });
                setTimeout(resolve, 500);
            });
        };

        const fadeIn = () => {
            display.textContent = art;
            display.style.color = dangerColor;
            display.style.textShadow = `0 0 6px ${dangerColor}40`;
            container.classList.remove('hidden');
            requestAnimationFrame(() => {
                container.style.opacity = '1';
            });
        };

        if (container.classList.contains('hidden')) {
            fadeIn();
        } else {
            fadeOut().then(fadeIn);
        }
    },

    _hash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash |= 0;
        }
        return hash;
    },
};

window.ASCIIManager = ASCIIManager;
