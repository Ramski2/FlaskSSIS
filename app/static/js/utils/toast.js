export function showToast(message, type = 'success', toastSelector = "#liveToast") {
    const toastLive = document.querySelector(toastSelector);

    if (!toastLive) {
        console.warn("Toast not found:", toastSelector);
        return;
    }

    console.log("Toast Found:", toastLive);

    toastLive.className = 'toast';
    toastLive.classList.add(`text-bg-${type}`, 'border-0');

    const toastBody = toastLive.querySelector('.toast-body');
        if (toastBody) {
            toastBody.textContent = message;
        } else {
            console.warn('No .toast-body found in:', toastSelector);
        }

    const toastInstance = bootstrap.Toast.getOrCreateInstance(toastLive, {delay: 7000, autohide: true});
    toastInstance.show();
}