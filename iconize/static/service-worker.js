let CACHE_NAME = VERSION;
self.addEventListener('install', e => {
  e.waitUntil(
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
  let cacheWhitelist = [CACHE_NAME];
  e.waitUntil(
      caches.keys().then((cacheNames) => {
          return Promise.all(
              cacheNames.map((cacheName) => {
                  if (cacheWhitelist.indexOf(cacheName) === -1) {
                      return caches.delete(cacheName);
                  }
              })
          );
      })
  );
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
