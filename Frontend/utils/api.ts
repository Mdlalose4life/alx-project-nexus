const API_BASE_URL = 'https://alx-project-nexus-b00y.onrender.com/api/v1';

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

export async function makeApiCall<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers: defaultHeaders,
    });

    const data = await response.json();

    return {
      data: response.ok ? data : undefined,
      error: !response.ok ? (data.message || data.error || 'Request failed') : undefined,
      status: response.status,
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Network error',
      status: 500,
    };
  }
}