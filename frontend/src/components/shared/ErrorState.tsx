import { AlertCircle } from 'lucide-react';
import Button from '@/components/ui/Button';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export default function ErrorState({
  message = 'Something went wrong. Please try again.',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <AlertCircle className="mb-4 h-12 w-12 text-red-400" />
      <h3 className="mb-1 text-lg font-semibold text-gray-900">
        Error loading data
      </h3>
      <p className="mb-6 max-w-sm text-sm text-gray-500">{message}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  );
}
