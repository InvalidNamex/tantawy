/**
 * Modern Theme Toggle React Component
 * A reusable theme toggle switch that can be placed anywhere
 * 
 * Features:
 * - Smooth animations with CSS transitions
 * - Sun/Moon icons that rotate and scale
 * - Modern minimal UI styling
 * - Rounded switch design
 * - Tailwind CSS classes (can be converted to plain CSS)
 * - React state management with useState
 * - Applies theme class to root element
 */

import React, { useState, useEffect } from 'react';

const ThemeToggle = ({ className = '' }) => {
  // State management - tracks current theme (light/dark)
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Initialize theme from localStorage on component mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const isDark = savedTheme === 'dark';
    setIsDarkMode(isDark);
    
    // Apply theme class to root element (html)
    document.documentElement.className = isDark ? 'dark' : 'light';
  }, []);

  // Handle theme toggle
  const toggleTheme = () => {
    const newIsDarkMode = !isDarkMode;
    setIsDarkMode(newIsDarkMode);
    
    // Update root element class
    const newTheme = newIsDarkMode ? 'dark' : 'light';
    document.documentElement.className = newTheme;
    
    // Save to localStorage for persistence
    localStorage.setItem('theme', newTheme);
    
    // Optional: Trigger custom event for other components
    window.dispatchEvent(new CustomEvent('themeChange', { 
      detail: { theme: newTheme } 
    }));
  };

  return (
    <div className={`theme-toggle-container ${className}`}>
      {/* Main toggle button */}
      <button
        onClick={toggleTheme}
        className="theme-toggle-switch focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        aria-label={`Switch to ${isDarkMode ? 'light' : 'dark'} mode`}
        aria-pressed={isDarkMode}
      >
        {/* Toggle track - the background rail */}
        <div 
          className={`
            toggle-track relative w-15 h-8 rounded-full transition-all duration-300 ease-out
            ${isDarkMode 
              ? 'bg-gradient-to-r from-gray-700 to-gray-600 border-gray-500' 
              : 'bg-gradient-to-r from-blue-100 to-blue-200 border-blue-200'
            }
            border-2 shadow-inner
          `}
        >
          {/* Toggle thumb - the sliding circle with icons */}
          <div 
            className={`
              toggle-thumb absolute top-0.5 w-6 h-6 rounded-full 
              flex items-center justify-center transition-all duration-300 ease-out
              transform shadow-lg
              ${isDarkMode 
                ? 'translate-x-7 bg-gradient-to-r from-blue-400 to-blue-500' 
                : 'translate-x-0.5 bg-gradient-to-r from-yellow-400 to-yellow-500'
              }
              hover:shadow-xl active:scale-95
            `}
          >
            {/* Sun Icon - visible in light mode */}
            <svg
              className={`
                w-3 h-3 text-white transition-all duration-300 absolute
                ${isDarkMode 
                  ? 'opacity-0 scale-75 rotate-180' 
                  : 'opacity-100 scale-100 rotate-0'
                }
              `}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                clipRule="evenodd"
              />
            </svg>

            {/* Moon Icon - visible in dark mode */}
            <svg
              className={`
                w-3 h-3 text-white transition-all duration-300 absolute
                ${isDarkMode 
                  ? 'opacity-100 scale-100 rotate-0' 
                  : 'opacity-0 scale-75 rotate-180'
                }
              `}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
              />
            </svg>
          </div>
        </div>
      </button>
      
      {/* Optional text label */}
      <span className="sr-only">
        Current theme: {isDarkMode ? 'Dark' : 'Light'} mode
      </span>
    </div>
  );
};

export default ThemeToggle;

/**
 * Usage Examples:
 * 
 * 1. Basic usage:
 * <ThemeToggle />
 * 
 * 2. With custom styling:
 * <ThemeToggle className="ml-4" />
 * 
 * 3. In a navigation bar:
 * <nav className="flex items-center justify-between p-4">
 *   <div>Logo</div>
 *   <ThemeToggle />
 * </nav>
 * 
 * 4. Listen to theme changes in other components:
 * useEffect(() => {
 *   const handleThemeChange = (event) => {
 *     console.log('Theme changed to:', event.detail.theme);
 *   };
 *   window.addEventListener('themeChange', handleThemeChange);
 *   return () => window.removeEventListener('themeChange', handleThemeChange);
 * }, []);
 * 
 * CSS Variables for custom styling (add to your global CSS):
 * :root {
 *   --color-light-bg: #ffffff;
 *   --color-light-text: #000000;
 * }
 * 
 * .dark {
 *   --color-light-bg: #1a1a1a;
 *   --color-light-text: #ffffff;
 * }
 * 
 * body {
 *   background-color: var(--color-light-bg);
 *   color: var(--color-light-text);
 *   transition: background-color 0.3s ease, color 0.3s ease;
 * }
 */