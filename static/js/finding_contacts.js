findNewContactsSocket.onmessage = function(e) {
  const contacts = JSON.parse(e.data).contacts;
  newContactsUl.innerHTML = "";

  modifyAvailableChats(true);
  toggleHiddeNewContactsDiv(false);

  if (contacts.length) {
    contacts.forEach((contact) => {
      const htmlContent = generateItem(contact, true)
      newContactsUl.innerHTML += htmlContent;
    })
  } else {
    const htmlContent = generateItem(null, true)
    newContactsUl.innerHTML = htmlContent;
  }
};


findNewContactInput.addEventListener("input", ()=>{
  if (findNewContactInput.value) {
    findNewContactsSocket.send(
      JSON.stringify({"username": findNewContactInput.value})
    );
  } else {
    toggleHiddeNewContactsDiv(true);
    modifyAvailableChats(false);
  }
});
