/**
 * LEDStripRenderer - Renders LED strip visualization to HTML5 Canvas
 * 
 * This class handles the visualization of LED strip data from Berry WASM module.
 * It receives frame buffer data as hex strings (ARGB format) and renders them
 * to a canvas element with configurable LED size and direction.
 */
class LEDStripRenderer {
  /**
   * Create a new LED strip renderer
   * @param {string} canvasId - ID of the canvas element to render to
   * @param {number} width - Number of LEDs in horizontal direction
   * @param {number} height - Number of LEDs in vertical direction (default 1 for strip)
   * @param {Object} options - Optional configuration
   * @param {number} options.pixelSize - Size of each LED in pixels (default 10)
   * @param {boolean} options.reversed - If true, render right-to-left (default false)
   * @param {number} options.ledSpacing - Gap between LEDs in pixels (default 2)
   * @param {string} options.backgroundColor - Background color (default '#1a1a1a')
   */
  constructor(canvasId, width, height = 1, options = {}) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) {
      throw new Error(`Canvas element with id '${canvasId}' not found`);
    }
    
    this.ctx = this.canvas.getContext('2d');
    this.width = width;
    this.height = height;
    
    // Configuration options with defaults
    this.pixelSize = options.pixelSize || 10;
    this.reversed = options.reversed || false;
    this.ledSpacing = options.ledSpacing || 2;
    this.backgroundColor = options.backgroundColor || '#000000';  // Pure black default
    
    // Calculate canvas dimensions
    this._updateCanvasSize();
    
    // Pre-create image data for efficient rendering
    this.imageData = this.ctx.createImageData(
      this.canvas.width,
      this.canvas.height
    );
    
    // Fill with background color initially
    this.clear();
  }
  
  /**
   * Update canvas size based on LED count and pixel size
   * @private
   */
  _updateCanvasSize() {
    const ledTotalSize = this.pixelSize + this.ledSpacing;
    this.canvas.width = this.width * ledTotalSize - this.ledSpacing;
    this.canvas.height = this.height * ledTotalSize - this.ledSpacing;
  }

  /**
   * Reconfigure the renderer with new dimensions
   * @param {number} width - New LED width
   * @param {number} height - New LED height
   */
  resize(width, height = 1) {
    this.width = width;
    this.height = height;
    this._updateCanvasSize();
    this.imageData = this.ctx.createImageData(
      this.canvas.width,
      this.canvas.height
    );
    this.clear();
  }
  
  /**
   * Clear the canvas with background color
   */
  clear() {
    this.ctx.fillStyle = this.backgroundColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Reset image data to background
    const bgColor = this._parseColor(this.backgroundColor);
    const data = this.imageData.data;
    for (let i = 0; i < data.length; i += 4) {
      data[i] = bgColor.r;
      data[i + 1] = bgColor.g;
      data[i + 2] = bgColor.b;
      data[i + 3] = 255;
    }
  }
  
  /**
   * Parse CSS color string to RGB components
   * @private
   * @param {string} colorStr - CSS color string (e.g., '#1a1a1a')
   * @returns {Object} Object with r, g, b properties
   */
  _parseColor(colorStr) {
    if (colorStr.startsWith('#')) {
      const hex = colorStr.slice(1);
      return {
        r: parseInt(hex.substring(0, 2), 16),
        g: parseInt(hex.substring(2, 4), 16),
        b: parseInt(hex.substring(4, 6), 16)
      };
    }
    return { r: 26, g: 26, b: 26 }; // Default dark background
  }
  
  /**
   * Render LED strip from hex string (ARGB format)
   * 
   * The hex string contains 8 characters per LED in ARGB format:
   * - Characters 0-1: Alpha (00-FF)
   * - Characters 2-3: Red (00-FF)
   * - Characters 4-5: Green (00-FF)
   * - Characters 6-7: Blue (00-FF)
   * 
   * @param {string} hexString - Hex string containing ARGB color data
   */
  renderFromHex(hexString) {
    // Clear to background first
    this.clear();
    
    // Parse hex string to colors (8 hex chars = 4 bytes = 1 ARGB color)
    const colors = [];
    for (let i = 0; i < hexString.length; i += 8) {
      const hex = hexString.substring(i, i + 8);
      if (hex.length === 8) {
        const color = parseInt(hex, 16);
        colors.push(color);
      }
    }
    
    // Render each LED
    for (let i = 0; i < colors.length; i++) {
      const x = i % this.width;
      const y = Math.floor(i / this.width);
      this.drawLED(x, y, colors[i]);
    }
    
    // Put the image data to canvas
    this.ctx.putImageData(this.imageData, 0, 0);
  }
  
  /**
   * Draw a single LED at the specified position
   * 
   * Converts ARGB (0xAARRGGBB) to RGBA for canvas rendering.
   * 
   * @param {number} x - X position in LED grid (0-based)
   * @param {number} y - Y position in LED grid (0-based)
   * @param {number} color - 32-bit ARGB color value
   */
  drawLED(x, y, color) {
    // Extract ARGB components from 32-bit color
    // Format: 0xAARRGGBB
    const a = (color >>> 24) & 0xFF;  // Use >>> for unsigned shift
    const r = (color >> 16) & 0xFF;
    const g = (color >> 8) & 0xFF;
    const b = color & 0xFF;
    
    // Calculate LED position on canvas
    const ledTotalSize = this.pixelSize + this.ledSpacing;
    let canvasX, canvasY;
    
    // If reversed, flip the x position
    if (this.reversed) {
      canvasX = (this.width - 1 - x) * ledTotalSize;
    } else {
      canvasX = x * ledTotalSize;
    }
    canvasY = y * ledTotalSize;
    
    // Draw the LED as a filled rectangle in the image data
    for (let dy = 0; dy < this.pixelSize; dy++) {
      for (let dx = 0; dx < this.pixelSize; dx++) {
        const px = canvasX + dx;
        const py = canvasY + dy;
        
        // Bounds check
        if (px >= 0 && px < this.canvas.width && 
            py >= 0 && py < this.canvas.height) {
          const idx = (py * this.canvas.width + px) * 4;
          
          // Set RGBA values (canvas uses RGBA, not ARGB)
          this.imageData.data[idx] = r;
          this.imageData.data[idx + 1] = g;
          this.imageData.data[idx + 2] = b;
          this.imageData.data[idx + 3] = a;
        }
      }
    }
  }

  /**
   * Set a single pixel color directly (for testing/debugging)
   * @param {number} index - LED index (0-based)
   * @param {number} color - 32-bit ARGB color value
   */
  setPixel(index, color) {
    const x = index % this.width;
    const y = Math.floor(index / this.width);
    this.drawLED(x, y, color);
    this.ctx.putImageData(this.imageData, 0, 0);
  }
  
  /**
   * Get the current LED count
   * @returns {number} Total number of LEDs
   */
  getLEDCount() {
    return this.width * this.height;
  }
  
  /**
   * Set whether the LED strip is reversed (right-to-left)
   * @param {boolean} reversed - true for right-to-left, false for left-to-right
   */
  setReversed(reversed) {
    this.reversed = !!reversed;
    this.clear();
  }
  
  /**
   * Set the pixel size for each LED
   * @param {number} size - Size in pixels
   */
  setPixelSize(size) {
    if (size < 1) {
      throw new Error("Pixel size must be at least 1");
    }
    this.pixelSize = size;
    this._updateCanvasSize();
    this.imageData = this.ctx.createImageData(
      this.canvas.width,
      this.canvas.height
    );
    this.clear();
  }
}

/**
 * Global function for Berry to call via js.call()
 * This is the bridge function that Berry code uses to render LED data
 * 
 * @param {string} hexString - Hex string containing ARGB color data
 */
window.renderLEDStrip = function(hexString) {
  if (window.ledRenderer) {
    window.ledRenderer.renderFromHex(hexString);
  } else {
    console.warn('LEDStripRenderer not initialized. Call initLEDRenderer() first.');
  }
};

/**
 * Initialize the global LED renderer
 * 
 * @param {string} canvasId - ID of the canvas element
 * @param {number} width - Number of LEDs horizontally
 * @param {number} height - Number of LEDs vertically (default 1)
 * @param {Object} options - Optional configuration
 * @returns {LEDStripRenderer} The initialized renderer instance
 */
window.initLEDRenderer = function(canvasId, width, height = 1, options = {}) {
  window.ledRenderer = new LEDStripRenderer(canvasId, width, height, options);
  return window.ledRenderer;
};

/**
 * Resize the global LED renderer
 * 
 * @param {number} width - New LED width
 * @param {number} height - New LED height (default 1)
 */
window.resizeLEDRenderer = function(width, height = 1) {
  if (window.ledRenderer) {
    window.ledRenderer.resize(width, height);
  } else {
    console.warn('LEDStripRenderer not initialized. Call initLEDRenderer() first.');
  }
};
