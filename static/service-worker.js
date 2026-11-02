
/*
==========================================
WARD 42 FIX-IT
Progressive Web App Service Worker
==========================================
*/

// Change this version when cached app files change.
const CACHE_NAME = "ward42-shell-v3";

// Essential public application files.
const APP_SHELL = [
    "/",
    "/static/offline.html",
    "/static/css/style.css",
    "/static/manifest.webmanifest",
    "/static/icons/icon-192.png",
    "/static/icons/icon-512.png",
    "/static/icons/icon-maskable-512.png",
    "/static/images/neighbourhood.svg",
    "/static/js/dashboard.js",
    "/static/js/reports.js",
    "/static/js/report_form.js",
    "/static/js/report_success.js"
];

const PUBLIC_ASSETS = new Set(
    APP_SHELL.filter(function (path) {
        return path.startsWith("/static/");
    })
);


// ==========================================
// INSTALL SERVICE WORKER
// ==========================================

self.addEventListener("install", function (event) {

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) {

                // Download the public app shell.
                return cache.addAll(APP_SHELL);

            })
            .then(function () {

                // Activate the new worker.
                return self.skipWaiting();

            })
    );

});


// ==========================================
// ACTIVATE SERVICE WORKER
// ==========================================

self.addEventListener("activate", function (event) {

    event.waitUntil(
        caches.keys()
            .then(function (cacheNames) {

                return Promise.all(

                    cacheNames
                        .filter(function (name) {

                            // Only delete outdated caches
                            // belonging to Ward 42 Fix-It.
                            return (
                                name.startsWith("ward42-shell-") &&
                                name !== CACHE_NAME
                            );

                        })
                        .map(function (name) {
                            return caches.delete(name);
                        })

                );

            })
            .then(function () {

                return self.clients.claim();

            })
    );

});


// ==========================================
// HANDLE NETWORK REQUESTS
// ==========================================

self.addEventListener("fetch", function (event) {

    const request = event.request;

    // Never interfere with submitted forms.
    if (request.method !== "GET") {
        return;
    }

    const url = new URL(request.url);

    // Only handle requests to our own website.
    if (url.origin !== self.location.origin) {
        return;
    }


    // ======================================
    // WEBPAGE NAVIGATION
    // ======================================

    if (request.mode === "navigate") {

        event.respondWith(

            // Try the real webpage first.
            fetch(request)
                .catch(async function () {

                    // If offline, display our custom page.
                    const cachedPage = await caches.match(
                        "/static/offline.html"
                    );

                    return cachedPage || Response.error();

                })

        );

        return;
    }


    // ======================================
    // CACHE PUBLIC APPLICATION FILES
    // ======================================

    if (PUBLIC_ASSETS.has(url.pathname)) {

        event.respondWith(

            caches.match(request)
                .then(function (cachedResponse) {

                    // Use the cached file when available.
                    if (cachedResponse) {
                        return cachedResponse;
                    }

                    // Otherwise request it normally.
                    return fetch(request);

                })

        );

    }

    // Private coordinator pages and JSON API
    // responses are never added to this cache.

});
