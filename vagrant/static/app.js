function logOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        $.get('/gdisconnect', function(data) {
            location.reload();
        });
    });
}

function onLoad() {
  gapi.load('auth2', function() {
    gapi.auth2.init();
  });
}