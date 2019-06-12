displayView = function(view){
  document.getElementById("view").innerHTML = document.getElementById(view).innerHTML;
}

window.onload = function(){
  usernameFound = false;
  if (localStorage.getItem("token") == null){
    localStorage.setItem("token", "[]");
  }
  else{
    var tokenJSON = localStorage.getItem("token");
    var tokenArray = JSON.parse(tokenJSON);

    if(tokenArray.token != null){
      currentView = "home";
      usernameFound = false;
      displayView("profileView");
      userInformation();
      refreshWall();
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
  var newUser = {email: email, password: password, firstname: firstName, familyname: familyName, gender: gender, city: city, country: country};

  if(password.localeCompare(repeatPassword) == 0){
    if(password.length >= 8 && password.length <= 20){
      var serverResult = serverstub.signUp(newUser);
      if(serverResult.success){
        document.getElementById("textSignUp").innerHTML = serverResult.message;
        serverResult = serverstub.signIn(email, password);
        if(serverResult.success){
          localStorage.setItem("token", "[]");
          var token = serverResult.data;
          var newToken = {username : email, token: token}
          localStorage.setItem("token", JSON.stringify(newToken));
          displayView("profileView");
          userInformation();
          currentView = "home"
        }
        else{
          document.getElementById("textSignUp").innerHTML = serverResult.message;
        }
      }
      else{
        document.getElementById("textSignUp").innerHTML = serverResult.message;
      }
    }
    else{
      document.getElementById("textSignUp").innerHTML = "Password size must be between 8 and 20 characters";
    }
  }
  else{
    document.getElementById("textSignUp").innerHTML = "Repeated password does not fit with the original";
  }
}

signInVaidator = function(){
  var username = document.getElementById("emailLogIn").value;
  var password = document.getElementById("passwordLogIn").value;
  var serverResult = serverstub.signIn(username, password);

  document.getElementById("textSignIn").innerHTML = serverResult.message;

  if(serverResult.success){
    localStorage.setItem("token", "[]");
    var token = serverResult.data;
    var newToken = {username : username, token: token}
    localStorage.setItem("token", JSON.stringify(newToken));
    currentView = "home";
    displayView("profileView");
    userInformation();
    refreshWall();
  }
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
  var tokenJSON = localStorage.getItem("token");
  var tokenArray = JSON.parse(tokenJSON);
  var oldPassword = document.getElementById("currentPassword").value;
  var newPassword = document.getElementById("newPassword").value;
  var repeatPassword = document.getElementById("repeatNewPassword").value;
  if(oldPassword.localeCompare(repeatPassword) != 0){
    if(newPassword.localeCompare(repeatPassword) == 0){
      if(newPassword.length >= 8 && newPassword.length <= 20){
        var serverResult = serverstub.changePassword(tokenArray.token, oldPassword, newPassword);
        document.getElementById("changePasswordResultText").innerHTML = serverResult.message;
      }else{
        document.getElementById("changePasswordResultText").innerHTML = "Password size must be between 8 and 20 characters";
      }
    }else{
      document.getElementById("changePasswordResultText").innerHTML = "Repeated password does not fit with the original";
    }
  }else{
    document.getElementById("changePasswordResultText").innerHTML = "Current password must be different to new password";
  }
}

signOut = function(){
  localStorage.setItem("token", "[]");
  currentView = "welcome";
  usernameFound = false;
  displayView("welcomeView");
}

userInformation = function(){
  var userDataJSON = localStorage.getItem("token");
  var username = JSON.parse(userDataJSON).username;
  var usersDataJSON = localStorage.getItem("users");
  var usersData = JSON.parse(usersDataJSON);
  document.getElementById("emailSignedInUser").innerHTML = usersData[username].email;
  document.getElementById("genderSignedInUser").innerHTML = usersData[username].gender;
  document.getElementById("countrySignedInUser").innerHTML = usersData[username].country;
  document.getElementById("familyNameSignedInUser").innerHTML = usersData[username].familyname;
  document.getElementById("firstNameSignedInUser").innerHTML = usersData[username].firstname;
  document.getElementById("citySignedInUser").innerHTML = usersData[username].city;
}

postComment = function(){
  var userDataJSON = localStorage.getItem("token");
  var token = JSON.parse(userDataJSON).token;
  var comment = "";
  var toEmail = "";

  if(currentView == "home"){
    comment = document.getElementById("userCommentBox").value;
    toEmail = JSON.parse(userDataJSON).username;
  }
  else{
    var comment = document.getElementById("otherUserCommentBox").value;
    if(usernameFound){
      toEmail = document.getElementById("usernameSearchInput").value;
    }
  }

  if(toEmail != ""){
    if(comment != ""){
      var serverResult = serverstub.postMessage(token, comment, toEmail);
      if(currentView == "home"){
        document.getElementById("resultText").innerHTML = serverResult.message;
      }
      else{
        document.getElementById("otherResultText").innerHTML = serverResult.message;
      }
    }
    else {
      if(currentView == "home"){
        document.getElementById("resultText").innerHTML = "You cannot post an empty message";
      }
      else{
        document.getElementById("otherResultText").innerHTML = "You cannot post an empty message";
      }
    }
  }
  else{
    document.getElementById("otherResultText").innerHTML = "No such user";
  }
}

refreshWall = function(){
  var signedInUserDataJSON = localStorage.getItem("token");
  var usersDataJSON = localStorage.getItem("users");
  var usersData = JSON.parse(usersDataJSON);
  var signedInUserData = JSON.parse(signedInUserDataJSON);
  var commentsString = [];
  var username = "";

  if(currentView == "home"){
    username = signedInUserData.username;
  }
  else{
    if(usernameFound){
      username = document.getElementById("usernameSearchInput").value;
    }
  }

  if(username != ""){
    var numberMessages = usersData[username].messages.length;

    if(numberMessages > 0){
      for(var commentIndex = 0; commentIndex < numberMessages; commentIndex++){
        var comment = usersData[username].messages[commentIndex];
        commentsString += comment.writer + ": " + comment.content + "\n";
      }
    }

    if(currentView == "home"){
      document.getElementById("userCommentsWall").value = commentsString;
    }
    else{
      document.getElementById("otherUserCommentsWall").value = commentsString;
    }
  }
  else{
    document.getElementById("otherResultText").innerHTML = "No such user";
  }
}

otherUserInformation = function(userInformation){
  document.getElementById("genderOtherUser").innerHTML = userInformation.gender;
  document.getElementById("countryOtherUser").innerHTML = userInformation.country;
  document.getElementById("familyNameOtherUser").innerHTML = userInformation.familyname;
  document.getElementById("firstNameOtherUser").innerHTML = userInformation.firstname;
  document.getElementById("cityOtherUser").innerHTML = userInformation.city;
}

searchUser = function(){
  var usernameSearched = document.getElementById("usernameSearchInput").value;
  var usersDataJSON = localStorage.getItem("users");
  var usersData = JSON.parse(usersDataJSON);
  var signedInUserDataJSON = localStorage.getItem("token");
  var signedInUsername = JSON.parse(signedInUserDataJSON).username;
  var distinctSignedInUser = usernameSearched != signedInUsername;
  var exists = usersData[usernameSearched] != undefined;
  if(exists && distinctSignedInUser){
    usernameFound = true;
    otherUserInformation(usersData[usernameSearched]);
    refreshWall();
  }
  else{
    document.getElementById("otherResultText").innerHTML = "No such user";
    usernameFound = false;
  }
}
