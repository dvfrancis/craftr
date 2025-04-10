/* Bootstrap toast notifications */

document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("toastMessage");
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
});
