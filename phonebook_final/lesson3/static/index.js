window.onload = function(){
   if (localStorage.getItem("contacts") == null){
     localStorage.setItem("contacts", "[]")
   }
}
saveContact = function(form){
   /*var contactsJSON = localStorage.getItem("contacts");
   var contactsArray = JSON.parse(contactsJSON);
   var newContact = {name : form.name.value, no : form.no.value}
   contactsArray.push(newContact);
   localStorage.setItem("contacts", JSON.stringify(contactsArray));*/

   var xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function(){
     if (this.readyState == 4 && this.status == 200){
        var resp = JSON.parse(xhr.responseText);
        if (resp.status){
          document.getElementById("feedback").innerHTML = "Contact saved!";
        }else{
          document.getElementById('feedback').innerHTML = "Something went wrong!";
        }
     }

   }
   xhr.open("PUT", "contact/save", true);
   xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
   xhr.send(JSON.stringify({'name' : form.name.value, 'number' : form.no.value}));
}
findContact = function(form){
  /*var contactsJSON = localStorage.getItem("contacts");
  var contactsArray = JSON.parse(contactsJSON);
  var showContacts = document.getElementById("showContacts");
  for ( var index in contactsArray){
    if (form.name.value == contactsArray[index].name){
       showContacts.innerHTML += "<p>" + contactsArray[index].name + "," + contactsArray[index].no + "</p>";
    }
  }*/

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
        contacts = JSON.parse(xhr.responseText);
        var showContacts = document.getElementById("showContacts");
        showContacts.innerHTML = "<ul>";
        for (var i in contacts){
            showContacts.innerHTML += "<li>" + contacts[i].name + " " + contacts[i].number +"</li>";
        }
        showContacts.innerHTML += "</ul>";
    }
  }

  xhr.open("GET", "contact/readbyname/" + form.name.value, true);
  xhr.send();
}
