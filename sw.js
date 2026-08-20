const CACHE_NAME = 'PCTools-v9';
const ASSETS = ['/', '/index.html', '/css/style.css'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (new URL(e.request.url).origin !== self.location.origin) return; // 타사(광고·분석 등) 요청은 그대로 통과
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
