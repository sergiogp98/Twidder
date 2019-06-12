window.onload = function(){
   if (localStorage.getItem("contacts") == null){
     localStorage.setItem("contacts", "[]")
   }
}

saveContact = function(form){
   var contactsJSON = localStorage.getItem("contacts");
   var contactsArray = JSON.parse(contactsJSON);
   var newContact = {name : form.name.value, no : form.no.value}
   contactsArray.push(newContact);
   localStorage.setItem("contacts", JSON.stringify(contactsArray));
}

findContact = function(form){
  var contactsJSON = localStorage.getItem("contacts");
  var contactsArray = JSON.parse(contactsJSON);
  var showContacts = document.getElementById("showContacts");
  for ( var index in contactsArray){
    if (form.name.value == contactsArray[index].name){
       showContacts.innerHTML += "<p>" + contactsArray[index].name + "," + contactsArray[index].no + "</p>";
    }
  }
}
