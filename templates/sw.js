self.addEventListener('push', function(event) {
    if (event.data) {
        const payload = event.data.json();
        const title = payload.title || 'Notification';
        const options = {
            body: payload.body || 'You have a new message.',
            icon: payload.icon || '/static/images/glocks_and_armor_logo.png',
            badge: payload.badge || '/static/images/glocks_and_armor_logo.png',
            vibrate: payload.vibrate || [200, 100, 200, 100, 200, 100, 200],
            requireInteraction: payload.requireInteraction !== undefined ? payload.requireInteraction : true,
            data: {
                url: payload.url || '/'
            }
        };

        event.waitUntil(self.registration.showNotification(title, options));
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    if (event.notification.data && event.notification.data.url) {
        event.waitUntil(
            clients.openWindow(event.notification.data.url)
        );
    }
});
