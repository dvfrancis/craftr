/**
 * Display a Bootstrap toast message on page load.
 *
 * This script waits for the DOM to fully load, retrieves the toast element
 * by its ID, initializes it using Bootstrap's Toast component, and displays it.
 */

document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("toastMessage");
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
});
