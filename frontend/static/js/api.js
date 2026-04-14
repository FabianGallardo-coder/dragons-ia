/**
 * Dragons & IA — api.js
 * Funciones fetch centralizadas para comunicarse con el backend.
 */

const API_BASE = '';  // Mismo origen

/**
 * Realiza un GET autenticado.
 */
async function apiGet(path) {
    const token = localStorage.getItem('dia_token');
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            'Authorization': token ? `Bearer ${token}` : '',
        },
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Error de conexión' }));
        throw new Error(err.detail || `Error ${res.status}`);
    }
    return res.json();
}

/**
 * Realiza un POST autenticado con body JSON.
 */
async function apiPost(path, body) {
    const token = localStorage.getItem('dia_token');
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify(body),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Error de conexión' }));
        throw new Error(err.detail || `Error ${res.status}`);
    }
    return res.json();
}

/**
 * Realiza un DELETE autenticado.
 */
async function apiDelete(path) {
    const token = localStorage.getItem('dia_token');
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'DELETE',
        headers: {
            'Authorization': token ? `Bearer ${token}` : '',
        },
    });
    if (!res.ok && res.status !== 204) {
        const err = await res.json().catch(() => ({ detail: 'Error de conexión' }));
        throw new Error(err.detail || `Error ${res.status}`);
    }
    return true;
}
