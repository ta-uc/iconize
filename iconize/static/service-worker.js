let CACHE_NAME = VERSION;
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
          cacheNames.map((cacheName) => {
            // If cacheName(oldcache) includes CACHENAME (newcache)
            if (cacheName.indexOf(CACHE_NAME.slice(0,32)) !== -1) {
              // Delete old matched cache.
              return caches.delete(cacheName);
            }
          })
      );
  }),
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll([
        './',
        './content/',
        './offlineErr/',
        './manifest.json',
        './static/style.css',
        './static/bootstrap.css',
        './static/main.js',
        './128.png',
        './256.png',
        './512.png'
      ]);
    })
  );
});

self.addEventListener('activate', e => {
});


self.addEventListener('fetch', event => {
  if (event.request.method !== "POST"){
    event.respondWith(
      caches.match(event.request).then(resp => {
        return resp || fetch(event.request).then(response => {
              return response;
        }).catch(()=>{
          return caches.match("./offlineErr/");
        });
      })
    );
  }
});
