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
      $("#status").text("Nectar instance ready! Launching container...");
      console.log("launching container on " + data);
      var image = "jupyter/datascience-notebook";
      $.ajax("http://" + data + ":8080", {
        type: "POST",
        data: {
          image: image
        },
        success: function(data, status, xhr) {
          var time = 3;
          setInterval(function(){
            $("#status").text("Container ready! Redirecting you in " + time);
            if (time == 0) {
              window.location.href = data;
            }
            time--;
          }, 1000);
        },
        error: function() {
          $("#status").text("Unable to launch " + image + " - is it accessible on Docker Hub?");
        }
      });
    },
    error: function() {
      $("#status").text("Login failed - check password?");
      $("#status").attr("class", "alert alert-danger");
    }
  });
});
