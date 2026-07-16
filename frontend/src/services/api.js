const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin);

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
 * Sends a query and streams progressive status notifications chunk-by-chunk using standard fetch and ReadableStream.
 * @param {string} queryText - The legal scenario/question.
 * @param {number} limit - The number of documents to retrieve.
 * @param {function} onProgress - Callback function that receives status events {"event": "status", "node": "...", "message": "..."}
 * @returns {Promise<Object>} The final QueryResponse result.
 */
export async function queryConstitutionStream(queryText, limit = 5, onProgress) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/query/stream`, {
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

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    let finalResult = null;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop(); // Keep last incomplete element

      for (const part of parts) {
        if (part.trim().startsWith('data:')) {
          const jsonStr = part.replace(/^data:\s*/, '').trim();
          if (!jsonStr) continue;
          try {
            const data = JSON.parse(jsonStr);
            if (data.event === 'status') {
              onProgress(data);
            } else if (data.event === 'final_result') {
              finalResult = data.data;
            } else if (data.event === 'error') {
              throw new Error(data.message);
            }
          } catch (e) {
            console.error('Error parsing SSE event:', e, jsonStr);
          }
        }
      }
    }

    // Flush remaining buffer
    if (buffer.trim().startsWith('data:')) {
      const jsonStr = buffer.replace(/^data:\s*/, '').trim();
      try {
        const data = JSON.parse(jsonStr);
        if (data.event === 'status') {
          onProgress(data);
        } else if (data.event === 'final_result') {
          finalResult = data.data;
        } else if (data.event === 'error') {
          throw new Error(data.message);
        }
      } catch (e) {
        // Safe to ignore
      }
    }

    if (!finalResult) {
      throw new Error('Streaming connection closed without delivering a final response.');
    }

    return finalResult;
  } catch (error) {
    console.error('API query stream error:', error);
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

/**
 * Fetches system information from the backend.
 * @returns {Promise<Object|null>} The system information JSON or null if request failed.
 */
export async function getSystemInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/system-info`);
    if (!response.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}
