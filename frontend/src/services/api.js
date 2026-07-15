const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Sends a query to the Constitution RAG multi-agent backend.
 * @param {string} queryText - The legal scenario/question.
 * @param {number} limit - The number of documents to retrieve.
 * @returns {Promise<Object>} The structured agentic search result.
 */
export async function queryConstitution(queryText, limit = 5) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: queryText,
        limit: limit,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server responded with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API query error:', error);
    throw error;
  }
}

/**
 * Checks the connection status and health of the FastAPI backend.
 * @returns {Promise<boolean>} True if the backend is healthy, otherwise false.
 */
export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === 'healthy';
  } catch {
    return false;
  }
}
