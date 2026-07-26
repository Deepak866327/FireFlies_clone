import Card from "@/components/ui/Card";

export default function ProfilePage() {
  return (
    <div className="mx-auto mt-6 max-w-xl">
      <h1 className="text-xl font-semibold text-gray-900">Profile</h1>

      <Card className="mt-6">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-gray-900 text-lg font-semibold text-white">
            D
          </div>
          <div>
            <p className="text-base font-semibold text-gray-900">Demo User</p>
            <p className="text-sm text-gray-500">demo@example.com</p>
          </div>
        </div>

        <dl className="mt-6 flex flex-col gap-3 text-sm">
          <div className="flex justify-between border-t border-gray-100 pt-3">
            <dt className="text-gray-500">Role</dt>
            <dd className="font-medium text-gray-900">Owner</dd>
          </div>
          <div className="flex justify-between border-t border-gray-100 pt-3">
            <dt className="text-gray-500">Authentication Status</dt>
            <dd className="font-medium text-gray-900">Demo User (No Authentication)</dd>
          </div>
        </dl>

        <p className="mt-6 rounded-md bg-gray-50 p-3 text-xs text-gray-500">
          This project assumes a default logged-in user for demonstration purposes.
        </p>
      </Card>
    </div>
  );
}
