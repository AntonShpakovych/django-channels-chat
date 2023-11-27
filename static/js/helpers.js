export function modifyAvailableContacts(isNewContact, availableContacts) {
  if (isNewContact) {
    availableContacts.classList.add("mt-3");
    availableContacts.style.height = "65%";
  } else {
    availableContacts.classList.remove("mt-3");
    availableContacts.style.height = "100%";
  }
}

export function toggleHiddeNewContactsDiv(needHide, newContactsDiv) {
  if (needHide) {
    newContactsDiv.style.display = "none";
  } else {
    newContactsDiv.style.display = "block";
  }
}

export function generateDataForContact(contact, isNewContact=false) {
  if (contact) {
    return `
          <li id="${contact.username}"  onmouseover="toggleActiveClass(this)" onclick="addNewContact(this)">
            <div class="d-flex bd-highlight">
              <div class="img_cont">
                <img src="" class="rounded-circle user_img">
                <span class="online_icon ${contact.is_online ? 'online' : 'offline'}"></span>
              </div>
              <div class="user_info">
                <span>${contact.username}</span>
                <p>${contact.is_online ? 'online': 'offline'}</p>
              </div>
            </div>
          </li>
    `;
  } else {
    return `
          <div style='color: white;' class='text-center'>
            Sorry, we did not find anything for your request.<br>
            P.S Try entering a valid username 😊
          </div>
    `
  }
}

