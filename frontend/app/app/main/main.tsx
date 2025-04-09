import { Header, LoginModal } from "./header";
import { Footer } from "./footer";
import { InputField } from "./input_field";
import { useState, useEffect } from 'react';
import { URL } from './cfg';

/// I just pass variables and callbacks to components in this tutorial.
/// This is not scalable if website gets bigger
/// More advanced approach is to use useContext, or state managers like Redux

export function Main() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showLoginModal, setShowLoginModal] = useState(false);

  // Check authentication status firstly on SPA load
  useEffect(() => {
    checkAuth();
  }, []);

  // functions
  const checkAuth = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${URL}/api/auth`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Important for sending cookies
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch(`${URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        return { success: true };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const logout = async () => {
    try {
      const response = await fetch(`${URL}/api/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (response.ok || response.status === 401 || response.status === 404) {
        setUser(null);
        window.location.reload(); // Refresh the page after logout
        return { success: true };
      } else {
        return { success: false, error: 'Logout failed' };
      }
    } catch (error) {
      console.error('Logout error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  // html
return (
    <div className="flex flex-col h-screen">
      {loading ? (
        <div className="flex-grow flex items-center justify-center">
          <p>Loading...</p>
        </div>
      ) : (
        <>
          <Header
            user={user}
            onLogoutClick={logout}
            onLoginClick={() => setShowLoginModal(true)}
          />
          <InputField />
          <Footer />
          {showLoginModal ?
              (<LoginModal
                onClose={() => setShowLoginModal(false)}
                onLogin={login}
              />) : (<></>)
          }
        </>
      )}
    </div>
  );
}
