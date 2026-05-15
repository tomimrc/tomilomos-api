interface BadgeProps {
  variant: 'active' | 'inactive';
  label?: string;
}

export default function Badge({ variant, label }: BadgeProps) {
  const text = label || (variant === 'active' ? 'Active' : 'Inactive');

  const styles = {
    active: 'bg-green-100 text-green-800',
    inactive: 'bg-gray-100 text-gray-600',
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${styles[variant]}`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          variant === 'active' ? 'bg-green-500' : 'bg-gray-400'
        }`}
      />
      {text}
    </span>
  );
}
