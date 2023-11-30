function generateItem(data= null, isNew= false) {
  if (data) {
    return `
          <li id="${isNew ? data.username : data.chat_id}"  onmouseover="addActiveClass(this)" onmouseout="removeActiveClass(this)" onclick="${isNew ? 'addNewChat(this)' : 'chatDetail(this)'}">
            <div class="d-flex bd-highlight">
              <div class="img_cont">
                <img src="${data.photo }" class="rounded-circle user_img">
                <span class="online_icon ${data.is_online ? 'online' : 'offline'}"></span>
              </div>
              <div class="user_info">
                <span>${data.username}</span>
                <p>${data.is_online ? 'online': 'offline'}</p>
              </div>
            </div>
          </li>
    `;
  } else {
    let message;

    if (isNew){
      message = `
          <div style='color: white;' class='text-center'>
            Sorry, we did not find anything for your request.<br>
            P.S Try entering a valid username 😊
          </div>
      `
    } else {
      message = `
          <div style='color: white;' class='text-center'>
            You don't have any chats.<br>
            P.S You should work on it 😊
          </div>
      `
    }

    return message
  }
}


function modifyAvailableChats(isNew) {
  if (isNew) {
    availableChats.classList.add("mt-3");
    availableChats.style.height = "65%";
  } else {
    availableChats.classList.remove("mt-3");
    availableChats.style.height = "100%";
  }
}


function addActiveClass(element) {
  element.classList.add("active");
}


function removeActiveClass(element) {
  element.classList.remove("active");
}


function toggleHiddeNewContactsDiv(needHide) {
  if (needHide) {
    newContactsDiv.style.display = "none";
  } else {
    newContactsDiv.style.display = "block";
  }
}


function generateChatHistory(messages){
  let htmlContent = ""

  messages.forEach((message) =>{

    let isCurrentUser = message.user === currentUserUsername
    htmlContent += functionGenerateMessage(message, isCurrentUser)
  })

  chatHistoryDiv.innerHTML = htmlContent
}


function functionGenerateMessage(data, isCurrentUser) {
  let date = transformDate(data.date)

  if (isCurrentUser) {
    return `<div class="d-flex justify-content-end mb-4 text-center">
    <div class="msg_container_send">
      ${data.text}
      <span class="msg_time_send">${date}</span>
    </div>
    <div class="img_cont_msg">
      <img
          src="${data.photo}"
          class="rounded-circle user_img_msg">
    </div>
  </div>`
  }
  return `<div class="d-flex justify-content-start mb-4 text-center">
    <div class="img_cont_msg">
      <img src="${data.photo}" class="rounded-circle user_img_msg">
    </div>
    <div class="msg_container">
      ${data.text}
      <span class="msg_time">${date}</span>
    </div>
  </div>`
}


function transformDate(date) {
  const old_date = new Date(date);

  const timeString = old_date.toLocaleTimeString([], { hour: "numeric", minute: "numeric" });

  const day = old_date.getDate().toString().padStart(2, "0");
  const month = (old_date.getMonth() + 1).toString().padStart(2, "0");
  const year = old_date.getFullYear();

  const dateString = `${day}/${month}/${year}`;

  return `${timeString}, ${dateString}`;
}


function generateChatHeader(title, quantity) {
  chatHeaderSpan.textContent = title
  chatHeaderP.textContent = `Messages ${quantity}`
}

function generateChatDetail(data){
  generateChatHeader(data.title, data.quantity)
  generateChatHistory(data.messages)
}


function updateQuantity(){
  const currentText = chatHeaderP.innerText;
  const currentNumber = parseInt(currentText.match(/\d+/)[0]);
  const newNumber = currentNumber + 1;
  chatHeaderP.innerText = currentText.replace(currentNumber, newNumber);
}
