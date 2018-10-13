const CACHE_NAME = 'v1';
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('CHACHE_NAME').then(function(cache) {
      return cache.addAll([
        '/static/style.css',
        '/static/main.js',
        '/static/bootstrap.js',
        '/static/bootstrap.css',
        '/static/summernote.js',
        '/static/summernote.css',
        './'
      ]);
    })
  );
});

self.addEventListener('activate', function(e) {
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

// self.addEventListener('fetch', function(event) {
//   if (event.request.method !== "POST"){
//     event.respondWith(
//       caches.match(event.request).then(function(resp) {
//         return resp || fetch(event.request).then(function(response) {
//             if(response.status === 200){
//             let responseClone = response.clone();
//             caches.open(CACHE_NAME).then(function(cache) {
//               cache.put(event.request, responseClone);
//             });
//           }
//           return response;
//         });
//       })
//     );
//     }
// });

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.open(CACHE_NAME).then(function(cache) {
      return fetch(event.request).then(function(response) {
        if (response.status === 200) {
          cache.put(event.request, response.clone());
        }
        return response;
      });
    })
  );
});