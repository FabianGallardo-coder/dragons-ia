/**
 * Dragons & IA - auth.js
 * Manejo de autenticacion JWT en localStorage.
 */

/**
 * Guarda el token y datos del usuario.
 */
function saveAuth(token, user) {
    localStorage.setItem('dia_token', token);
    localStorage.setItem('dia_user', JSON.stringify(user));
}

/**
 * Obtiene el usuario actual desde localStorage.
 */
function getUser() {
    const raw = localStorage.getItem('dia_user');
    if (!raw) return null;
    try {
        return JSON.parse(raw);
    } catch {
        return null;
    }
}

/**
 * Obtiene el token JWT solo si no esta expirado.
 * Verifica localmente el campo `exp` del payload sin llamar al servidor.
 */
function getToken() {
    const token = localStorage.getItem('dia_token');
    if (!token) return null;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        // exp esta en segundos UTC
        if (payload.exp && Date.now() / 1000 > payload.exp) {
            localStorage.removeItem('dia_token');
            localStorage.removeItem('dia_user');
            localStorage.removeItem('dia_active_save');
            return null;
        }
    } catch {
        localStorage.removeItem('dia_token');
        return null;
    }
    return token;
}

/**
 * Cierra sesion y limpia localStorage.
 */
function logout() {
    localStorage.removeItem('dia_token');
    localStorage.removeItem('dia_user');
    localStorage.removeItem('dia_active_save');
    localStorage.removeItem('dia_active_character');
    localStorage.removeItem('dia_pending_character');
    location.href = '/';
}

/**
 * Redirige al login si no hay sesion activa o el token expiro.
 */
function requireAuth() {
    if (!getToken()) {
        location.href = '/login.html?expired=1';
    }
}

/**
 * Guarda la configuracion de IA del jugador en localStorage.
 */
function saveGameConfig(config) {
    localStorage.setItem('dia_game_config', JSON.stringify(config));
}

/**
 * Obtiene la configuracion de IA guardada.
 */
function getGameConfig() {
    const raw = localStorage.getItem('dia_game_config');
    if (!raw) return {};
    try {
        return JSON.parse(raw);
    } catch {
        return {};
    }
}
