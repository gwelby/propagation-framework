/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * SERVICE WORKER — Offline Support for Propagation Framework Explorer
 * 
 * Caches all assets for offline use, provides background sync for analytics,
 * and serves fallback content when offline.
 * ═══════════════════════════════════════════════════════════════════════════════
 */

const CACHE_NAME = 'pf-explorer-v1';
const OFFLINE_CACHE = 'pf-explorer-offline-v1';
const ANALYTICS_CACHE = 'pf-analytics-v1';

// Core assets that must be cached for the app to work
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/derivation.css',
  '/derivation-graph.css',
  '/core.js',
  '/data.js',
  '/touch-controller.js',
  '/manifest.json',
  '/print.css',
  '/performance-engine.js',
  '/audio-engine.js',
  '/transition-engine.js',
  
  // Panel scripts
  '/panels/hub.js',
  '/panels/foundations.js',
  '/panels/refraction.js',
  '/panels/generations.js',
  '/panels/koide.js',
  '/panels/weinberg.js',
  '/panels/koide-weinberg-bridge.js',
  '/panels/god-equation.js',
  '/panels/bohr.js',
  '/panels/dashboard.js',
  '/panels/consciousness.js',
  
  // Additional scripts
  '/reality-correction.js',
  '/derivation-graph.js',
  
  // Vendor libraries
  '/vendor/three.min.js',
  '/vendor/OrbitControls.js',
  '/vendor/EffectComposer.js',
  '/vendor/RenderPass.js',
  '/vendor/ShaderPass.js',
  '/vendor/CopyShader.js',
  '/vendor/LuminosityHighPassShader.js',
  '/vendor/UnrealBloomPass.js',
  '/vendor/BokehShader.js',
  '/vendor/BokehPass.js',
  '/vendor/Tone.js',
  
  // Fonts
  '/vendor/fonts.css'
];

// Optional assets that enhance the experience
const OPTIONAL_ASSETS = [
  '/journey.html',
  '/comparison.html',
  '/derivation.html',
  '/playground.html',
  '/nogos.html',
  '/scale-ladder.html',
  '/belt-trick.html',
  '/journey.css',
  '/comparison.css',
  '/derivation.css',
  '/nogos.css',
  '/playground.css',
  '/scale-ladder.css',
  '/belt-trick.css',
  '/journey.js',
  '/comparison.js',
  '/derivation.js',
  '/derivation-3d.js',
  '/timeline.js',
  '/truth-utils.js',
  '/nogos.js',
  '/playground.js',
  '/scale-engine.js',
  '/propagation-shaders.js',
  '/postprocessing.js',
  '/cosmic-scene.js',
  '/planck-scene.js',
  '/scale-scenes.js',
  '/scale-ladder.js',
  '/belt-trick.js',
  '/assets/og-image.svg',
  '/assets/twitter-image.svg'
];

// ═══════════════════════════════════════════════════════════════════════════
// INSTALL EVENT — Cache core assets
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching core assets...');
        return cache.addAll(CORE_ASSETS)
          .then(() => cache.addAll(OPTIONAL_ASSETS).catch((error) => {
            console.warn('[SW] Optional cache population skipped:', error);
          }));
      })
      .then(() => {
        console.log('[SW] Core assets cached successfully');
        return caches.open(OFFLINE_CACHE);
      })
      .then((cache) => {
        // Create offline fallback page
        const offlinePage = new Response(
          `<!DOCTYPE html>
          <html lang="en">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Offline — PF Explorer</title>
            <style>
              body {
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #0a0a1a;
                color: #e8f0ff;
                font-family: system-ui, -apple-system, sans-serif;
                text-align: center;
                padding: 20px;
              }
              .container {
                max-width: 400px;
              }
              h1 {
                color: #00e5ff;
                margin-bottom: 16px;
              }
              p { line-height: 1.6; margin-bottom: 24px; }
              button {
                background: linear-gradient(135deg, #00e5ff, #44ff88);
                color: #0a0a1a;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
              }
              .icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 24px;
                background: radial-gradient(circle, rgba(0, 229, 255, 0.2) 0%, transparent 70%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <div class="icon">📡</div>
              <h1>You're Offline</h1>
              <p>The Propagation Framework Explorer works offline, but this page hasn't been cached yet. Try reloading or check your connection.</p>
              <button onclick="location.reload()">Try Again</button>
            </div>
          </body>
          </html>`,
          {
            headers: { 'Content-Type': 'text/html' }
          }
        );
        return cache.put('/offline.html', offlinePage);
      })
      .then(() => {
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Cache install failed:', error);
      })
  );
});

// ═══════════════════════════════════════════════════════════════════════════
// ACTIVATE EVENT — Clean up old caches
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => {
              // Delete old versions
              return name.startsWith('pf-explorer-') && 
                     name !== CACHE_NAME && 
                     name !== OFFLINE_CACHE;
            })
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Service worker activated');
        return self.clients.claim();
      })
  );
});

// ═══════════════════════════════════════════════════════════════════════════
// FETCH EVENT — Serve from cache or network
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip cross-origin requests (except for critical CDNs)
  if (url.origin !== self.location.origin) {
    return;
  }
  
  // Analytics/background sync handling
  if (url.pathname.includes('analytics') || url.pathname.includes('log')) {
    event.respondWith(handleAnalyticsRequest(request));
    return;
  }
  
  // Navigation requests (HTML pages)
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }
  
  // CSS/JS assets — Cache first, network fallback
  if (url.pathname.match(/\.(css|js)$/)) {
    event.respondWith(handleAssetRequest(request, 'cache-first'));
    return;
  }
  
  // Images — Cache first with network fallback
  if (url.pathname.match(/\.(png|jpg|jpeg|svg|gif|webp|ico)$/)) {
    event.respondWith(handleAssetRequest(request, 'cache-first'));
    return;
  }
  
  // Fonts — Cache first, long-term cache
  if (url.pathname.match(/\.(woff|woff2|ttf|otf|eot)$/)) {
    event.respondWith(handleAssetRequest(request, 'cache-first'));
    return;
  }
  
  // Default — Network first with cache fallback
  event.respondWith(handleDefaultRequest(request));
});

// ═══════════════════════════════════════════════════════════════════════════
// REQUEST HANDLERS
// ═══════════════════════════════════════════════════════════════════════════

// Handle navigation requests
async function handleNavigationRequest(request) {
  try {
    // Try network first for fresh content
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Navigation fetch failed, serving from cache');
    
    // Try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fall back to index.html (SPA behavior)
    const fallback = await caches.match('/index.html');
    if (fallback) {
      return fallback;
    }
    
    // Last resort — offline page
    return caches.match('/offline.html');
  }
}

// Handle asset requests
async function handleAssetRequest(request, strategy) {
  if (strategy === 'cache-first') {
    // Try cache first
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      // Update cache in background
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(request, networkResponse));
          }
        })
        .catch(() => {/* Ignore background update errors */});
      
      return cachedResponse;
    }
    
    // Fall back to network
    try {
      const networkResponse = await fetch(request);
      if (networkResponse && networkResponse.status === 200) {
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, networkResponse.clone());
      }
      return networkResponse;
    } catch (error) {
      console.error('[SW] Asset fetch failed:', error);
      // Return a minimal error response for CSS/JS
      if (request.url.endsWith('.css')) {
        return new Response('/* Failed to load */', { 
          headers: { 'Content-Type': 'text/css' } 
        });
      }
      if (request.url.endsWith('.js')) {
        return new Response('/* Failed to load */', { 
          headers: { 'Content-Type': 'application/javascript' } 
        });
      }
      throw error;
    }
  }
  
  // Default: network first
  return handleDefaultRequest(request);
}

// Handle default requests
async function handleDefaultRequest(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    throw error;
  }
}

// Handle analytics requests with background sync
async function handleAnalyticsRequest(request) {
  try {
    // Try to send immediately
    const response = await fetch(request);
    return response;
  } catch (error) {
    // Queue for background sync
    const cache = await caches.open(ANALYTICS_CACHE);
    const clone = request.clone();
    await cache.put(
      `/analytics-queue/${Date.now()}`,
      new Response(JSON.stringify({
        url: request.url,
        method: request.method,
        headers: Array.from(request.headers.entries()),
        timestamp: Date.now()
      }))
    );
    
    // Register for background sync if supported
    if ('sync' in self.registration) {
      self.registration.sync.register('analytics-sync');
    }
    
    // Return success to prevent errors
    return new Response(JSON.stringify({ queued: true }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// BACKGROUND SYNC
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('sync', (event) => {
  if (event.tag === 'analytics-sync') {
    event.waitUntil(syncAnalytics());
  }
});

async function syncAnalytics() {
  const cache = await caches.open(ANALYTICS_CACHE);
  const requests = await cache.keys();
  
  for (const request of requests) {
    if (request.url.includes('/analytics-queue/')) {
      try {
        const response = await cache.match(request);
        const data = await response.json();
        
        // Try to send the queued analytics
        await fetch(data.url, {
          method: data.method,
          headers: new Headers(data.headers)
        });
        
        // Remove from queue on success
        await cache.delete(request);
      } catch (error) {
        console.log('[SW] Analytics sync failed for item:', error);
        // Keep in queue for next sync
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// PUSH NOTIFICATIONS (for future use)
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'New content available',
    tag: 'pf-explorer-update',
    requireInteraction: false,
    actions: [
      { action: 'explore', title: 'Explore' },
      { action: 'dismiss', title: 'Dismiss' }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('PF Explorer', options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// ═══════════════════════════════════════════════════════════════════════════
// MESSAGE HANDLING (from main thread)
// ═══════════════════════════════════════════════════════════════════════════

self.addEventListener('message', (event) => {
  switch (event.data.type) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;
      
    case 'GET_CACHE_STATUS':
      getCacheStatus().then((status) => {
        event.ports[0].postMessage(status);
      });
      break;
      
    case 'CLEAR_CACHE':
      clearAllCaches().then(() => {
        event.ports[0].postMessage({ success: true });
      });
      break;
  }
});

async function getCacheStatus() {
  const cache = await caches.open(CACHE_NAME);
  const keys = await cache.keys();
  
  return {
    cached: keys.length,
    version: CACHE_NAME,
    quota: navigator.storage ? await navigator.storage.estimate() : null
  };
}

async function clearAllCaches() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames.map((name) => caches.delete(name))
  );
}

console.log('[SW] Service worker script loaded');
