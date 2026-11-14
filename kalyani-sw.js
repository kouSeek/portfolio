const CACHE_NAMES = ['kortex-books-v1', 'kalyani-cache-v1'];

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      // Also check matching by pathname without host
      try {
        const urlObj = new URL(req.url);
        const relPath = urlObj.pathname.replace(/^\/+/, '');
        return caches.match(relPath).then((relCached) => {
          if (relCached) return relCached;
          return fetch(req);
        });
      } catch (e) {
        return fetch(req);
      }
    }).catch(() => {
      // Offline fallback: try cache again or return books.html for navigation
      return caches.match(req).then((fallback) => {
        if (fallback) return fallback;
        if (req.mode === 'navigate') {
          return caches.match('books.html');
        }
        return new Response('Offline: file not cached', { status: 503, statusText: 'Offline' });
      });
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if ('focus' in client) return client.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow('./kalyani.html');
    })
  );
});
