/**
 * Theme Manager - Glassmorphism Design System
 * Tantawy Management System
 * 
 * Handles dark/light theme switching with localStorage persistence
 * and system preference detection
 */

class ThemeManager {
  constructor() {
    this.storageKey = 'tantawy-theme';
    this.themeAttribute = 'data-theme';
    this.theme = this.getInitialTheme();
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    this.init();
  }
  
  /**
   * Initialize the theme manager
   */
  init() {
    this.applyTheme(this.theme);
    this.bindEvents();
    this.watchSystemPreferences();
  }
  
  /**
   * Get the initial theme based on localStorage or system preference
   * @returns {string} 'light' or 'dark'
   */
  getInitialTheme() {
    // Check localStorage first
    const savedTheme = localStorage.getItem(this.storageKey);
    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      return savedTheme;
    }
    
    // Fall back to system preference
    return this.mediaQuery.matches ? 'dark' : 'light';
  }
  
  /**
   * Apply the theme to the document
   * @param {string} theme - 'light' or 'dark'
   */
  applyTheme(theme) {
    this.theme = theme;
    
    // Apply theme attribute to document element
    document.documentElement.setAttribute(this.themeAttribute, theme);
    
    // DEBUGGING: Also set on body for redundancy
    document.body.setAttribute(this.themeAttribute, theme);
    
    // DEBUGGING: Force text color changes that will be visible over background images
    if (theme === 'dark') {
      // Dark theme: make all text white/light
      document.body.style.color = '#ffffff';
      // Apply to common text elements
      const textSelectors = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'a', 'button', 'label', 'td', 'th', 'li', '.nav-link', '.navbar-brand'];
      textSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
          el.style.setProperty('color', '#ffffff', 'important');
        });
      });
    } else {
      // Light theme: make all text black/dark  
      document.body.style.color = '#212529';
      // Apply to common text elements
      const textSelectors = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'a', 'button', 'label', 'td', 'th', 'li', '.nav-link', '.navbar-brand'];
      textSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
          el.style.setProperty('color', '#212529', 'important');
        });
      });
    }
    
    // Save to localStorage
    localStorage.setItem(this.storageKey, theme);
    
    // Update theme toggle button
    this.updateToggleButton(theme);
    
    // Update meta theme-color for mobile browsers
    this.updateMetaThemeColor(theme);
    
    // Dispatch custom event for other components
    this.dispatchThemeChangeEvent(theme);
  }
  
  /**
   * Toggle between light and dark themes
   */
  toggleTheme() {
    const newTheme = this.theme === 'light' ? 'dark' : 'light';
    this.applyTheme(newTheme);
  }
  
  /**
   * Set a specific theme
   * @param {string} theme - 'light' or 'dark'
   */
  setTheme(theme) {
    if (theme === 'light' || theme === 'dark') {
      this.applyTheme(theme);
    }
  }
  
  /**
   * Get the current theme
   * @returns {string} Current theme
   */
  getCurrentTheme() {
    return this.theme;
  }
  
  /**
   * Bind event listeners
   */
  bindEvents() {
    // Theme toggle button
    const toggleBtn = document.getElementById('theme-toggle');
    
    if (toggleBtn) {
      toggleBtn.addEventListener('click', (e) => {
        this.toggleTheme();
      });
    }
    
    // Keyboard shortcut (Ctrl/Cmd + Shift + T)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
        e.preventDefault();
        this.toggleTheme();
      }
    });
    
    // Handle any theme toggle elements
    document.addEventListener('click', (e) => {
      if (e.target.matches('[data-theme-toggle]')) {
        e.preventDefault();
        this.toggleTheme();
      }
    });
  }
  
  /**
   * Watch for system preference changes
   */
  watchSystemPreferences() {
    this.mediaQuery.addEventListener('change', (e) => {
      // Only change theme if user hasn't manually set a preference
      const savedTheme = localStorage.getItem(this.storageKey);
      if (!savedTheme) {
        const systemTheme = e.matches ? 'dark' : 'light';
        this.applyTheme(systemTheme);
      }
    });
  }
  
  /**
   * Update the theme toggle button appearance
   * @param {string} theme - Current theme
   */
  updateToggleButton(theme) {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;
    
    // Update ARIA attributes
    toggleBtn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    toggleBtn.setAttribute('aria-label', 
      theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'
    );
    
    // Update screen reader text
    const srText = toggleBtn.querySelector('.sr-only');
    if (srText) {
      srText.textContent = `Current theme: ${theme === 'dark' ? 'Dark' : 'Light'}`;
    }
    
    // Update button class for styling
    toggleBtn.classList.toggle('dark-mode', theme === 'dark');
  }
  
  /**
   * Update meta theme-color for mobile browsers
   * @param {string} theme - Current theme
   */
  updateMetaThemeColor(theme) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    
    if (!metaThemeColor) {
      metaThemeColor = document.createElement('meta');
      metaThemeColor.name = 'theme-color';
      document.head.appendChild(metaThemeColor);
    }
    
    // Set appropriate color based on theme
    const color = theme === 'dark' ? '#0f1419' : '#ffffff';
    metaThemeColor.content = color;
  }
  
  /**
   * Dispatch custom theme change event
   * @param {string} theme - New theme
   */
  dispatchThemeChangeEvent(theme) {
    const event = new CustomEvent('themechange', {
      detail: { 
        theme: theme,
        previousTheme: this.theme === 'light' ? 'dark' : 'light'
      }
    });
    document.dispatchEvent(event);
  }
  
  /**
   * Add smooth transition class to prevent flash during theme change
   */
  addTransition() {
    const css = `
      *, *::before, *::after {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
      }
    `;
    
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    
    // Remove transition after animation completes
    setTimeout(() => {
      document.head.removeChild(style);
    }, 300);
  }
  
  /**
   * Preload theme-specific images to prevent flash
   */
  preloadThemeImages() {
    const images = [
      // Add any theme-specific image URLs here
    ];
    
    images.forEach(url => {
      const img = new Image();
      img.src = url;
    });
  }
  
  /**
   * Auto-save theme preference on page unload
   */
  autoSave() {
    window.addEventListener('beforeunload', () => {
      localStorage.setItem(this.storageKey, this.theme);
    });
  }

  /**
   * Add visual debugging indicator
   */
  addDebugIndicator() {
    // Create debug indicator element
    const debugDiv = document.createElement('div');
    debugDiv.id = 'theme-debug-indicator';
    debugDiv.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: #ff4444;
      color: white;
      padding: 10px;
      border-radius: 5px;
      font-family: monospace;
      font-size: 12px;
      z-index: 9999;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    
    debugDiv.innerHTML = `
      <div><strong>Theme Debug</strong></div>
      <div>Current: <span id="debug-current-theme">${this.theme}</span></div>
      <div>HTML attr: <span id="debug-html-attr">${document.documentElement.getAttribute('data-theme') || 'none'}</span></div>
      <div>Body attr: <span id="debug-body-attr">${document.body.getAttribute('data-theme') || 'none'}</span></div>
      <div>localStorage: <span id="debug-storage">${localStorage.getItem(this.storageKey) || 'none'}</span></div>
    `;
    
    // Remove existing debug indicator if present
    const existing = document.getElementById('theme-debug-indicator');
    if (existing) {
      existing.remove();
    }
    
    document.body.appendChild(debugDiv);
  }

  /**
   * Update visual debugging indicator
   */
  updateDebugIndicator() {
    const currentSpan = document.getElementById('debug-current-theme');
    const htmlSpan = document.getElementById('debug-html-attr');
    const bodySpan = document.getElementById('debug-body-attr');
    const storageSpan = document.getElementById('debug-storage');
    
    if (currentSpan) currentSpan.textContent = this.theme;
    if (htmlSpan) htmlSpan.textContent = document.documentElement.getAttribute('data-theme') || 'none';
    if (bodySpan) bodySpan.textContent = document.body.getAttribute('data-theme') || 'none';
    if (storageSpan) storageSpan.textContent = localStorage.getItem(this.storageKey) || 'none';
    
    // Update theme test element
    const themeDisplay = document.getElementById('current-theme-display');
    if (themeDisplay) {
      themeDisplay.textContent = this.theme;
    }
  }
}

/**
 * Utility functions for theme management
 */
const ThemeUtils = {
  /**
   * Check if dark mode is preferred by system
   * @returns {boolean}
   */
  isDarkModePreferred() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  },
  
  /**
   * Check if reduced motion is preferred
   * @returns {boolean}
   */
  isReducedMotionPreferred() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },
  
  /**
   * Check if high contrast is preferred
   * @returns {boolean}
   */
  isHighContrastPreferred() {
    return window.matchMedia('(prefers-contrast: high)').matches;
  },
  
  /**
   * Get current theme from document
   * @returns {string}
   */
  getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  },
  
  /**
   * Check if current theme is dark
   * @returns {boolean}
   */
  isDarkTheme() {
    return this.getCurrentTheme() === 'dark';
  }
};

// Initialize theme manager when DOM is ready
let themeManager;

document.addEventListener('DOMContentLoaded', () => {
  themeManager = new ThemeManager();
  
  // Add global theme utilities to window for easy access
  window.ThemeManager = themeManager;
  window.ThemeUtils = ThemeUtils;
  
  // Auto-save theme on page unload
  themeManager.autoSave();
  
  // Preload theme images
  themeManager.preloadThemeImages();
});

// Handle theme changes from other tabs/windows
window.addEventListener('storage', (e) => {
  if (e.key === 'tantawy-theme' && e.newValue && themeManager) {
    themeManager.setTheme(e.newValue);
  }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ThemeManager, ThemeUtils };
}

// Additional theme-related event listeners
document.addEventListener('themechange', (e) => {
  // Handle theme change in other components
  // Update any theme-dependent components here
  updateThemeDependentComponents(e.detail.theme);
});

/**
 * Update components that depend on theme
 * @param {string} theme - New theme
 */
function updateThemeDependentComponents(theme) {
  // Update charts if any
  updateChartsTheme(theme);
  
  // Update maps if any
  updateMapsTheme(theme);
  
  // Update any third-party components
  updateThirdPartyTheme(theme);
}

/**
 * Update charts theme (placeholder for chart libraries)
 * @param {string} theme - New theme
 */
function updateChartsTheme(theme) {
  // Implementation for chart theme updates
  // This would integrate with chart libraries like Chart.js, D3, etc.
}

/**
 * Update maps theme (placeholder for map libraries)
 * @param {string} theme - New theme
 */
function updateMapsTheme(theme) {
  // Implementation for map theme updates
  // This would integrate with map libraries like Leaflet, Google Maps, etc.
}

/**
 * Update third-party components theme
 * @param {string} theme - New theme
 */
function updateThirdPartyTheme(theme) {
  // Update any third-party components that need theme awareness
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager();
});