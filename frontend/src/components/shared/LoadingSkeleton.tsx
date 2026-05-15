interface SkeletonProps {
  variant?: 'table-row' | 'card';
  rows?: number;
}

export default function LoadingSkeleton({
  variant = 'table-row',
  rows = 5,
}: SkeletonProps) {
  if (variant === 'card') {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: rows }).map((_, i) => (
          <div
            key={i}
            className="animate-pulse rounded-xl border border-gray-200 p-5"
          >
            <div className="mb-3 h-5 w-3/4 rounded bg-gray-200" />
            <div className="mb-2 h-4 w-1/2 rounded bg-gray-100" />
            <div className="h-4 w-1/3 rounded bg-gray-100" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200">
      <table className="w-full">
        <thead className="border-b bg-gray-50">
          <tr>
            {Array.from({ length: 4 }).map((_, i) => (
              <th key={i} className="px-4 py-3">
                <div className="h-4 w-20 animate-pulse rounded bg-gray-200" />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: rows }).map((_, rowIdx) => (
            <tr key={rowIdx} className="border-b">
              {Array.from({ length: 4 }).map((_, colIdx) => (
                <td key={colIdx} className="px-4 py-3">
                  <div
                    className={`h-4 animate-pulse rounded bg-gray-100 ${
                      colIdx === 0 ? 'w-40' : 'w-24'
                    }`}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
