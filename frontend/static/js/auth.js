/**
 * Dragons & IA — auth.js
 * Manejo de autenticación JWT en localStorage.
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
 * Obtiene el token JWT.
 */
function getToken() {
    return localStorage.getItem('dia_token');
}

/**
 * Cierra sesión y limpia localStorage.
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
 * Redirige al login si no hay sesión activa.
 */
function requireAuth() {
    if (!getToken()) {
        location.href = '/login.html';
    }
}

/**
 * Guarda la configuración de IA del jugador en localStorage.
 */
function saveGameConfig(config) {
    localStorage.setItem('dia_game_config', JSON.stringify(config));
}

/**
 * Obtiene la configuración de IA guardada.
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
