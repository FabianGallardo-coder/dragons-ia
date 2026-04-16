/**
 * Dragons & IA — api.js
 * Funciones fetch centralizadas para comunicarse con el backend.
 */

const API_BASE = '';  // Mismo origen

/**
 * Wrapper de fetch con retry para errores transitorios (502, 503, 504, network).
 */
async function _fetchWithRetry(url, options, retries = 2) {
    for (let attempt = 0; attempt <= retries; attempt++) {
        try {
            const res = await fetch(url, options);
            // Reintentar en errores de servidor transitorios
            if (attempt < retries && (res.status === 502 || res.status === 503 || res.status === 504)) {
                await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
                continue;
            }
            return res;
        } catch (err) {
            // Error de red (offline, timeout, etc.)
            if (attempt < retries) {
                await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
                continue;
            }
            throw new Error('Sin conexión a internet. Verificá tu red e intentá de nuevo.');
        }
    }
}

/**
 * Realiza un GET autenticado.
 */
async function apiGet(path) {
    const token = localStorage.getItem('dia_token');
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const res = await _fetchWithRetry(`${API_BASE}${path}`, { headers });
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
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const res = await _fetchWithRetry(`${API_BASE}${path}`, {
        method: 'POST',
        headers,
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
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const res = await _fetchWithRetry(`${API_BASE}${path}`, {
        method: 'DELETE',
        headers,
    });
    if (!res.ok && res.status !== 204) {
        const err = await res.json().catch(() => ({ detail: 'Error de conexión' }));
        throw new Error(err.detail || `Error ${res.status}`);
    }
    return true;
}
