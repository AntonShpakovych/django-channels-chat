import { modifyAvailableContacts, toggleHiddeNewContactsDiv, generateDataForContact } from './helpers.js';

const addNewContactInput = document.getElementById("find-new-contacts").querySelector("input");
const findNewContactsSocket = new WebSocket(`ws://${window.location.host}/ws/contacts/find/new/`);

let availableContacts = document.getElementById("available-contacts");

let newContactsDiv = document.getElementById("new-contacts");
let newContactsUl = newContactsDiv.querySelector("ul");


findNewContactsSocket.onmessage = function(e) {
  const contacts = JSON.parse(e.data).contacts;
  newContactsUl.innerHTML = "";

  modifyAvailableContacts(true, availableContacts);
  toggleHiddeNewContactsDiv(false, newContactsDiv);

  if (contacts.length) {
    contacts.forEach((contact) => {
      const htmlContent = generateDataForContact(contact, true)
      newContactsUl.innerHTML += htmlContent;
    })
  } else {
    const htmlContent = generateDataForContact()
    newContactsUl.innerHTML = htmlContent;
  }
};


addNewContactInput.addEventListener("input", ()=>{
  if (addNewContactInput.value) {
    findNewContactsSocket.send(
      JSON.stringify({"username": addNewContactInput.value})
    );
  } else {
    toggleHiddeNewContactsDiv(true, newContactsDiv);
    modifyAvailableContacts(false, availableContacts);
  }
});
