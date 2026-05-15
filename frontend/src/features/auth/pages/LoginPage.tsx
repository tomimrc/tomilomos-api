import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { ChefHat, Loader2 } from 'lucide-react';
import { login } from '@/api/auth';
import { useAuthStore } from '@/stores/authStore';

const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email format'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

interface JwtPayload {
  sub: string;
  tenant_id: string;
  exp: number;
  iat: number;
  jti: string;
}

function decodeJwtPayload(token: string): JwtPayload {
  const payload = token.split('.')[1];
  return JSON.parse(atob(payload));
}

export default function LoginPage() {
  const navigate = useNavigate();
  const token = useAuthStore((s) => s.token);
  const setAuth = useAuthStore((s) => s.setAuth);

  const [serverError, setServerError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    resetField,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '' },
  });

  // Already authenticated → redirect
  useEffect(() => {
    if (token) {
      navigate('/app/dashboard', { replace: true });
    }
  }, [token, navigate]);

  const onSubmit = async (values: LoginFormValues) => {
    setServerError(null);
    setLoading(true);

    try {
      const response = await login(values.email, values.password);

      const payload = decodeJwtPayload(response.access_token);
      setAuth(response.access_token, payload.tenant_id, payload.sub);
      navigate('/app/dashboard', { replace: true });
    } catch (err: unknown) {
      const axiosErr = err as {
        response?: { status?: number; data?: { detail?: string } };
        request?: unknown;
      };

      if (axiosErr.response) {
        const status = axiosErr.response.status;
        if (status === 401) {
          setServerError('Invalid email or password');
          resetField('password');
        } else if (status === 500) {
          setServerError('Server error. Please try again later.');
        } else {
          setServerError(
            axiosErr.response.data?.detail || 'An unexpected error occurred.'
          );
        }
      } else if (axiosErr.request) {
        setServerError('Connection failed. Check your network and try again.');
      } else {
        setServerError('An unexpected error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.97 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.35, ease: 'easeOut' }}
        className="w-full max-w-sm"
      >
        {/* Card */}
        <div className="rounded-2xl border border-gray-200 bg-white px-6 py-8 shadow-lg sm:px-8">
          {/* Branding */}
          <div className="mb-6 flex flex-col items-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-600 shadow-md">
              <ChefHat className="h-7 w-7 text-white" />
            </div>
            <h1 className="mt-3 text-xl font-bold text-gray-900">
              TomiLomos
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Sign in to your account
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label
                htmlFor="email"
                className="mb-1 block text-sm font-medium text-gray-700"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="alice@example.com"
                className={`w-full rounded-lg border px-3 py-2 text-sm transition-colors placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 ${
                  errors.email
                    ? 'border-red-300 focus:ring-red-500'
                    : 'border-gray-300'
                }`}
                {...register('email')}
              />
              {errors.email && (
                <p className="mt-1 text-xs text-red-600">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-1 block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                autoComplete="current-password"
                placeholder="••••••••"
                className={`w-full rounded-lg border px-3 py-2 text-sm transition-colors placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 ${
                  errors.password
                    ? 'border-red-300 focus:ring-red-500'
                    : 'border-gray-300'
                }`}
                {...register('password')}
              />
              {errors.password && (
                <p className="mt-1 text-xs text-red-600">
                  {errors.password.message}
                </p>
              )}
            </div>

            {/* Server error */}
            <AnimatePresence mode="wait">
              {serverError && (
                <motion.div
                  key="error"
                  initial={{ opacity: 0, y: -6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -6 }}
                  transition={{ duration: 0.2 }}
                  className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700"
                >
                  <p>{serverError}</p>
                  {serverError.includes('network') && (
                    <button
                      type="button"
                      onClick={() => setServerError(null)}
                      className="mt-1 text-xs font-medium text-red-600 underline hover:text-red-800"
                    >
                      Dismiss
                    </button>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition-all hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading && <Loader2 className="h-4 w-4 animate-spin" />}
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="mt-4 text-center text-xs text-gray-400">
          TomiLomos v1.0 — Gastronomic Management
        </p>
      </motion.div>
    </div>
  );
}
