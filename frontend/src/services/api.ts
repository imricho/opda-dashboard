const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8088'

export async function apiGet<T>(path: String, token?: string): Promise<T> {
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        }
    });

    if (!res.ok) {
        const text = await res.text()
        throw new Error(`Get ${path} failed: ${res.status} ${text}`);
    }

    return (await res.json()) as T;
}