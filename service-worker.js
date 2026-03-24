const CACHE_NAME = 'uganda-digital-platform-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/app.py'
];

// تثبيت Service Worker وتخزين الملفات مؤقتاً
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// جلب الملفات من التخزين المؤقت إذا كانت متاحة
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // إذا وجد الملف في التخزين المؤقت، أعد منه
        if (response) {
          return response;
        }
        // وإلا، اجلبه من الشبكة
        return fetch(event.request);
      })
  );
});

// تحديث التخزين المؤقت عند توفر إصدار جديد
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
