displayView = function(view){
  document.getElementById("view").innerHTML = document.getElementById(view).innerHTML;
}

window.onload = function(){
  usernameFound = false;
  if (localStorage.getItem("token") == null){
    localStorage.setItem("token", "[]");
  }
  else{
    var userDataJSON = localStorage.getItem("token");
    var userData = JSON.parse(userDataJSON);
    if(userData.length != 0){ //User stukk loggued in
      clientSocket(userData.username);
      currentView = "home";
      usernameFound = false;
      displayView("profileView");
      userInformation(userData.username, userData.token);
    }
    else{
      currentView = "welcome";
      usernameFound = false;
      displayView("welcomeView");
    }
  }
}



signUpValidator = function(){
  var email = document.getElementById("emailSignUp").value;
  var password = document.getElementById("passwordSignUp").value;
  var repeatPassword = document.getElementById("repeatPassword").value;
  var firstName = document.getElementById("firstName").value;
  var familyName = document.getElementById("familyName").value;
  var gender = document.getElementById("gender").value;
  var city = document.getElementById("city").value;
  var country = document.getElementById("country").value;

  if(password.localeCompare(repeatPassword) != 0) {
    document.getElementById("textSignUp").innerHTML = "Repeated password does not fit with the original";
    return;
  }

  if(password.length < 8 || password.length > 20) {
    document.getElementById("textSignUp").innerHTML = "Password size must be between 8 and 20 characters";
    return;
  }

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      document.getElementById("textSignUp").innerHTML = resp.message;
    }
  }

  xhr.open("POST", "sign-up", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.send(JSON.stringify({'email': email, 'password': password, 'firstname': firstName, 'familyname': familyName, 'gender': gender, 'city': city, 'country': country}));
}

signInVaidator = function(){
  var username = document.getElementById("emailLogIn").value;
  var password = document.getElementById("passwordLogIn").value;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      document.getElementById("textSignIn").innerHTML = resp.message;
      if(resp.success){
        console.log("publicKey" ,resp['publicKey']);
        var newToken = {'username': username, 'token':resp['token'],'publicKey':resp['publicKey']}
        localStorage.setItem("token",JSON.stringify(newToken));
        clientSocket(username);
        currentView = "home";
        displayView("profileView");
        userInformation(username,resp['token']);
        refreshWall();
      }
    }
  }

  xhr.open("POST", "sign-in", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.send(JSON.stringify({'email' : username, 'password' : password}));
}

displayPanel = function(button){
  if(button === "Home"){
    document.getElementById("homePanel").style.display = "block";
    document.getElementById("browsePanel").style.display = "none";
    document.getElementById("accountPanel").style.display = "none";
    currentView = "home";
  }
  else if(button === "Browse"){
    document.getElementById("homePanel").style.display = "none";
    document.getElementById("browsePanel").style.display = "block";
    document.getElementById("accountPanel").style.display = "none";
    currentView = "browse";
  }
  else{
    document.getElementById("homePanel").style.display = "none";
    document.getElementById("browsePanel").style.display = "none";
    document.getElementById("accountPanel").style.display = "block";
    currentView = "account";
  }
}

changePassword = function(){
  var oldPassword = document.getElementById("currentPassword").value;
  var newPassword = document.getElementById("newPassword").value;
  var repeatPassword = document.getElementById("repeatNewPassword").value;

  if(newPassword.localeCompare(repeatPassword) != 0){
    document.getElementById("changePasswordResultText").innerHTML = "Repeated password does not fit with the original";
    return;
  }

  if(newPassword.length < 8 || newPassword.length > 20){
    document.getElementById("changePasswordResultText").innerHTML = "Password size must be between 8 and 20 characters";
    return;
  }

  var token = JSON.parse(localStorage.getItem("token")).token;
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      document.getElementById("changePasswordResultText").innerHTML = resp.message;
    }
  }

  xhr.open("PUT", "change-password", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  cToken= md5(token+oldPassword+newPassword);
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken);
  xhr.send(JSON.stringify({'oldPassword' : oldPassword, 'newPassword' : newPassword, 'publicKey':publicKey}));
}

signOut = function(){
  console.log("signOut pasa por aqui");
  var token = JSON.parse(localStorage.getItem("token")).token;
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      console.log("entra");
      var resp = JSON.parse(xhr.responseText);
      console.log("Respuesta",resp.success);
      if(resp.success){
        currentView = "welcome";
        usernameFound = false;
        localStorage.removeItem("token");
        displayView("welcomeView");

      }
      else console.log("??? failure to log out ???");
    }
  }

  xhr.open("POST", "sign-out", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  cToken = md5(token);
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken );
  xhr.send(JSON.stringify({'publicKey':publicKey}));
}

userInformation = function(username,token){
  console.log(token);
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  cToken = md5(token);
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      if(resp.success){
        if(currentView == "home"){
          //clientSocket(username);
          document.getElementById("emailSignedInUser").innerHTML = resp['data']['email'];
          document.getElementById("genderSignedInUser").innerHTML = resp['data']['gender'];
          document.getElementById("countrySignedInUser").innerHTML = resp['data']['country'];
          document.getElementById("familyNameSignedInUser").innerHTML = resp['data']['familyname'];
          document.getElementById("firstNameSignedInUser").innerHTML = resp['data']['firstname'];
          document.getElementById("citySignedInUser").innerHTML = resp['data']['city'];
        }
        else{
          console.log(resp);
          //clientSocket(username);
          document.getElementById("genderOtherUser").innerHTML = resp['data']['gender'];
          document.getElementById("countryOtherUser").innerHTML = resp['data']['country'];
          document.getElementById("familyNameOtherUser").innerHTML = resp['data']['familyname'];
          document.getElementById("firstNameOtherUser").innerHTML = resp['data']['firstname'];
          document.getElementById("cityOtherUser").innerHTML = resp['data']['city'];
        }
      }
    }
  }
  var variable = publicKey
  console.log(variable);
  xhr.open("GET", "/get-data/"+variable, true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken);
  xhr.send();
}

postComment = function(){
  var comment = "";
  var toEmail = "";
  var token = JSON.parse(localStorage.getItem("token")).token;
  if(currentView == "home"){
    comment = document.getElementById("userCommentBox").value;
    toEmail = JSON.parse(localStorage.getItem("token")).username;
  }
  else{
    comment = document.getElementById("otherUserCommentBox").value;
    if(usernameFound){
      toEmail = document.getElementById("usernameSearchInput").value;
    }
  }

  if(toEmail == ""){
    document.getElementById("otherResultText").innerHTML = "No such user";
    return;
  }


  if(comment == ""){
    if(currentView == "home"){
      document.getElementById("resultText").innerHTML = "You cannot post an empty message";
    }
    else{
      document.getElementById("otherResultText").innerHTML = "You cannot post an empty message";
    }
    return;
  }
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      if(resp.success){
        if(currentView == "home"){
          document.getElementById("resultText").innerHTML = resp.message;
        }
        else{
          document.getElementById("otherResultText").innerHTML = resp.message;
        }
      }
    }
  }
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  xhr.open("POST", "message", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  cToken = md5(token,comment,toEmail);
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken);
  xhr.send(JSON.stringify({'message' : comment, 'email' : toEmail,'publicKey':publicKey}));
}

refreshWall = function(){
  var toemail = "";
  var token = JSON.parse(localStorage.getItem("token")).token;

  if(currentView == "home"){
    toemail = JSON.parse(localStorage.getItem("token")).username;
  }
  else{
    if(usernameFound){
      toemail = document.getElementById("usernameSearchInput").value;
    }
    else{
      document.getElementById("otherResultText").innerHTML = "No such user";
      return;
    }
  }
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var resp = JSON.parse(xhr.responseText);
      if(resp.success){
        var commentsString = [];
        var numberMessages = resp['data'].length;
        if(numberMessages > 0){
          for(var commentIndex = numberMessages-1; commentIndex >=0; commentIndex--){
            var comment = resp['data'][commentIndex];
            commentsString += comment['email_sender'] + ": " + comment['message'] + "\n";
          }
          if(currentView == "home"){
            document.getElementById("userCommentsWall").value = commentsString;
          }
          else{
            document.getElementById("otherUserCommentsWall").value = commentsString;
          }
        }
      }
    }
  }
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  var cToken = md5(token);
  var variable = publicKey;
  xhr.open("POST", "get-data/message/"+ variable, true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken);
  xhr.send(JSON.stringify({'email':toemail}));
}

searchUser = function(){
  var username = document.getElementById("usernameSearchInput").value;
  var token = JSON.parse(localStorage.getItem("token")).token;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status){
      var resp = JSON.parse(xhr.responseText);
      if(resp.success){
        usernameFound = true;
        userInformation(username,token);
        console.log(username);
        refreshWall();
      }
    }
  }
  var publicKey = JSON.parse(localStorage.getItem("token")).publicKey;
  var cToken = md5(token)
  var variable = publicKey

  xhr.open("GET", "get-data/"+ variable, true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.setRequestHeader('Authorization', 'Bearer ' + cToken);
  xhr.send();
}

function clientSocket(email){

  console.log("clientSocket called with token: " + email);

  /*var email = localStorage.getItem("token").username;
  var token = localStorage.getItem("token").token;
  console.log(email);
  console.log(token);*/

  var socket = new WebSocket("ws://localhost:5000/api");

  socket.onopen = function(){
    socket.send(email);
  }

  socket.onerror = function(error){
    console.log("WS Error: " +error);
  }
  socket.onmessage = function(event){
    console.log("WS tells me to sign out maybe ", event.data);
    if(event.data == "sign_out"){
      currentView = "welcome";
      usernameFound = false;
      localStorage.removeItem("token");
      displayView("welcomeView");
    }
  }

}
