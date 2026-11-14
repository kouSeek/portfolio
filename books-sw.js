// Books Library Service Worker — Offline Flight & Travel Cache
const CACHE_NAME = 'kortex-books-v1';

const PRECACHE_URLS = [
  './books.html',
  './assets/books_catalog.json',
  './assets/books_text_vault.json',
  './assets/icons/favicon-hub.png'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        console.warn('[books-sw] Some precache items could not be loaded immediately:', err);
      });
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME && k.startsWith('kortex-books-')) {
            return caches.delete(k);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // If fetching books assets or audio or html, try cache first, fall back to network, and cache new responses
  if (
    url.pathname.includes('/audio/books/') ||
    url.pathname.includes('/assets/books_') ||
    url.pathname.endsWith('books.html')
  ) {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) {
          // Return cached response immediately
          return cached;
        }
        return fetch(req)
          .then((networkResp) => {
            if (networkResp && networkResp.status === 200) {
              const respClone = networkResp.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(req, respClone);
              });
            }
            return networkResp;
          })
          .catch(() => {
            // Offline and not in cache
            if (req.destination === 'document') {
              return caches.match('./books.html');
            }
            return new Response('Offline: Content not cached yet', { status: 503, statusText: 'Offline' });
          });
      })
    );
  }
});
