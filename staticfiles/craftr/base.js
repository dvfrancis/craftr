/* global bootstrap */

/**
 * Display a Bootstrap toast message on page load.
 *
 * This script waits for the DOM to fully load, retrieves the toast element
 * by its ID, initializes it using Bootstrap's Toast component, and displays it.
 */

document.addEventListener('DOMContentLoaded', () => {
  let toastElement = document.getElementById('toastMessage');
  if (toastElement) {
    let toast = new bootstrap.Toast(toastElement);
    toast.show();
  }
});