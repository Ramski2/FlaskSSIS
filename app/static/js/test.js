const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
const toastBody = toastLiveExample.querySelector('.toast-body');
if (toastBody) {
            toastBody.textContent = "You're gonna die";
        } else {
            console.warn('No .toast-body found in:', toastSelector);
        }


if (toastTrigger) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
  toastTrigger.addEventListener('click', () => {
    toastBootstrap.show()
  })
}