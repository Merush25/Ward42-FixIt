
/*
==========================================
WARD 42 FIX-IT
PWA Service Worker Registration
==========================================
*/

if ("serviceWorker" in navigator) {

    window.addEventListener("load", async function () {

        try {

            // Register the service worker.
            const registration =
                await navigator.serviceWorker.register(
                    "/service-worker.js",
                    {
                        scope: "/"
                    }
                );

            console.log(
                "Ward 42 Service Worker registered:",
                registration.scope
            );

        } catch (error) {

            console.error(
                "Service Worker registration failed:",
                error
            );

        }

    });

} else {

    console.log(
        "This browser does not support Service Workers."
    );

}
