// Set a timeout to close the alarm msg after 2 seconds
setTimeout(function () {
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
  }, 2000);