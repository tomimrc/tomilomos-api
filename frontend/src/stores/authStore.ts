import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  tenantId: string | null;
  userId: string | null;
  setAuth: (token: string, tenantId: string, userId: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      tenantId: null,
      userId: null,
      setAuth: (token, tenantId, userId) => set({ token, tenantId, userId }),
      logout: () => set({ token: null, tenantId: null, userId: null }),
    }),
    {
      name: 'tomilomos-auth',
    }
  )
);
