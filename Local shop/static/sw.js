// Service Worker for Local Shop
const CACHE_NAME = 'local-shop-v10';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/locations.js',
    '/static/favicon.svg',
    '/static/icon-192.png',
    '/static/icon-512.png',
    '/manifest.json'
];

self.addEventListener('install', (event) => {
    // Force this service worker to become the active service worker
    self.skipWaiting();
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Caching assets...');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .catch((error) => {
                console.error('Failed to cache assets:', error);
            })
    );
});

self.addEventListener('activate', (event) => {
    // Claim clients immediately so the page is controlled by the SW without reload
    event.waitUntil(self.clients.claim());
    
    // Clean up old caches
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Network first, fall back to cache strategy
    event.respondWith(
        fetch(event.request)
            .catch(() => {
                return caches.match(event.request);
            })
    );
});