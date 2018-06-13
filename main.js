$("#login").submit(function(e) {
  e.preventDefault();
  $("#status").show();
  $("#status").text("Logging in...");
  $("#status").attr("class", "alert alert-primary");
  var username = $("#username").val();
  var pw = $("#password").val();
  console.log("submit", username, pw);
  $.ajax("launch", {
    type: "POST",
    data: {
      username: username,
      password: pw
    },
    success: function(data, status, xhr) {
      console.log(data, status, xhr);
      var time = 3;
      setInterval(function(){
        $("#status").text("Nectar instance ready! Redirecting you in " + time);
        if (time == 0) {
          window.location.href = "http://" + data;
        }
        time--;
      }, 1000);
    },
    error: function() {
      $("#status").text("Login failed - check password?");
      $("#status").attr("class", "alert alert-danger");
    }
  });
});
