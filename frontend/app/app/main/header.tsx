import { useState } from 'react';
import { URL } from './cfg';

export function LoginModal({ onClose, onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true); // is login modal (otherwise signup modal)
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent default event behavior
    setError('');

    if (isLogin) {
      const result = await onLogin(email, password);
      if (result.success) {
        onClose();
      } else {
        setError(result.error);
      }
    } else {
      // Signup
      try {
        const response = await fetch(`${URL}/api/user`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
          const result = await onLogin(email, password);
          if (result.success) {
            onClose();
          } else {
            setError(`Account created but login failed: ${result.error}`);
          }
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Signup failed');
        }
      } catch (error) {
        setError(`Can't signup: ${error}`);
      }
    }
  };

  return (
    <div className="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">{isLogin ? 'Login' : 'Sign Up'}</h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              className="w-full px-3 py-2 border rounded-lg"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              className="w-full px-3 py-2 border rounded-lg"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="flex items-center justify-between mb-4">
            <button
              type="submit"
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg"
            >
              {isLogin ? 'Login' : 'Sign Up'}
            </button>

            <button
              type="button"
              className="text-green-500 hover:text-green-600"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Create new account" : 'Already have an account?'}
            </button>
          </div>
        </form>

        <div className="text-right">
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export function Header({ user, onLogoutClick, onLoginClick }) {
  return (
    <header className="bg-green-200 text-gray-900 p-4 flex justify-between items-center shadow-md">
      <h1 className="text-xl font-semibold">Test app</h1>
      {user ? (
        <div className="flex items-center gap-4">
          <span className="text-gray-800">{user.email}</span>
          <button
            onClick={onLogoutClick}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
          >
            Logout
          </button>
        </div>
      ) : (
        <button
          onClick={onLoginClick}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
        >
          Login
        </button>
      )}
    </header>
  );
};
