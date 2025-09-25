import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Set a default timeout (in milliseconds)
const DEFAULT_TIMEOUT = 8000 // 8 seconds

class ApiService {
  constructor() {
    this.instance = axios.create({
      baseURL: process.env.baseUrl,
      timeout: DEFAULT_TIMEOUT
    });

    // Track if popup is already active
    this.errorPopupActive = false;
    this.errorPopup = null;

    this.instance.interceptors.response.use(
      response => response,
      error => {
        if (error.code === 'ECONNABORTED' && !this.errorPopupActive) {
          this.showTimeoutError();
        }
        return Promise.reject(error);
      }
    );
  }

  showTimeoutError() {
    // Return if popup already exists
    if (this.errorPopupActive) return;

    // Create pop-up container
    const popup = document.createElement('div');
    
    // Main container styles
    popup.style.position = 'fixed';
    popup.style.top = '20px';
    popup.style.left = '50%';
    popup.style.transform = 'translateX(-50%)';
    popup.style.padding = '20px 30px';
    popup.style.backgroundColor = '#ff4444';
    popup.style.color = 'white';
    popup.style.borderRadius = '6px';
    popup.style.zIndex = '10000';
    popup.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    popup.style.fontFamily = 'Arial, sans-serif';
    popup.style.fontSize = '16px';
    popup.style.textAlign = 'center';
    popup.style.maxWidth = '600px';
    popup.style.width = '90%';
    popup.style.display = 'flex';
    popup.style.alignItems = 'center';
    popup.style.justifyContent = 'space-between';
    popup.style.gap = '20px';

    // Error message
    const message = document.createElement('div');
    message.textContent = 'Error: Database connection timed out. Please check your connection and try again later.';
    message.style.flex = '1';
    message.style.wordBreak = 'break-word';

    // Close button
    const closeButton = document.createElement('button');
    closeButton.textContent = '×';
    closeButton.style.background = 'transparent';
    closeButton.style.border = 'none';
    closeButton.style.color = 'white';
    closeButton.style.fontSize = '24px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.padding = '0 0 4px 10px';
    closeButton.style.lineHeight = '1';
    
    // Close handler
    closeButton.addEventListener('click', () => {
      popup.style.opacity = '0';
      setTimeout(() => {
        if (popup.parentNode) {
          document.body.removeChild(popup);
        }
        this.errorPopupActive = false;
        this.errorPopup = null;
      }, 300);
    });

    popup.appendChild(message);
    popup.appendChild(closeButton);

    // Fade-in animation
    popup.style.opacity = '0';
    popup.style.transition = 'opacity 0.3s ease-in-out';
    
    document.body.appendChild(popup);
    
    setTimeout(() => {
      popup.style.opacity = '1';
    }, 10);

    // Set active state
    this.errorPopupActive = true;
    this.errorPopup = popup;
  }

  request(method, url, data = {}, config = {}) {
    // Merge the default timeout with any config timeout
    const mergedConfig = {
      timeout: DEFAULT_TIMEOUT,
      ...config
    }
    
    return this.instance({
      method,
      url,
      data,
      ...mergedConfig
    })
  }

  get(url, config = {}) {
    return this.request('GET', url, {}, config)
  }

  post(url, data, config = {}) {
    return this.request('POST', url, data, config)
  }

  put(url, data, config = {}) {
    return this.request('PUT', url, data, config)
  }

  patch(url, data, config = {}) {
    return this.request('PATCH', url, data, config)
  }

  delete(url, data = {}, config = {}) {
    return this.request('DELETE', url, data, config)
  }
}

export default new ApiService()