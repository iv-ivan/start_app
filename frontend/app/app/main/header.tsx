export function Header() {
  return (
    <header className="bg-green-200 text-gray-900 p-4 flex justify-between items-center shadow-md">
      <h1 className="text-xl font-semibold">Test app</h1>
      <button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition">
        Login
      </button>
    </header>
  );
};
