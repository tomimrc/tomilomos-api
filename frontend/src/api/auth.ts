import axios from 'axios';
import type { TokenResponse } from '@/types/auth';

// Dedicated axios instance WITHOUT the apiClient interceptors.
// Using apiClient for login would cause a redirect loop on 401.
const authApi = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export async function login(
  email: string,
  password: string
): Promise<TokenResponse> {
  const { data } = await authApi.post<TokenResponse>('/auth/login', {
    email,
    password,
  });
  return data;
}
