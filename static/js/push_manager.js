// static/js/push_manager.js

const vapidPublicKeyEndpoint = '/users/vapid_public_key/';
const saveSubscriptionEndpoint = '/users/save_push_subscription/';

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

async function subscribeUserToPush() {
    try {
        if (!('serviceWorker' in navigator)) {
            console.warn('Service workers are not supported.');
            return;
        }
        if (!('PushManager' in window)) {
            console.warn('Push notifications are not supported.');
            return;
        }

        // Wait for service worker registration to be ready
        const registration = await navigator.serviceWorker.ready;

        // Get VAPID public key from backend
        const response = await fetch(vapidPublicKeyEndpoint);
        const data = await response.json();
        const applicationServerKey = urlB64ToUint8Array(data.public_key);

        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: applicationServerKey
        });

        // Send subscription to backend
        await fetch(saveSubscriptionEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(subscription)
        });

        console.log('User is subscribed to push notifications.');

    } catch (error) {
        console.error('Failed to subscribe the user: ', error);
    }
}

async function initializePushNotifications() {
    if ('serviceWorker' in navigator) {
        try {
            await navigator.serviceWorker.register('/sw.js');
            console.log('Service Worker is registered');
            
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                subscribeUserToPush();
            } else {
                console.warn('Notification permission denied.');
            }
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    }
}

// Ensure the function is exposed globally
window.initializePushNotifications = initializePushNotifications;

// Automatically initialize if the user is authenticated (can be triggered from HTML)
document.addEventListener('DOMContentLoaded', () => {
    // Only call initializePushNotifications if the user is a staff member.
    // This will be controlled in base.html.
});
