const newConversationInput = document.getElementById("filter-new-conversation").querySelector("input");
const newConversationSocket = new WebSocket(`ws://${window.location.host}/ws/chats/new_conversation/`);

let availableConversation = document.getElementById("available-conversation");
let newConversationDiv = document.getElementById("new-conversation");
let newConversationUl = newConversationDiv.querySelector("ul");


newConversationSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  const users = JSON.parse(data.users);

  newConversationUl.innerHTML = "";

  modifyAvailableConversation(isNewConversation=true);
  toggleHiddeNewConversationDiv(needHide=false);

  if (users.length) {
    users.forEach((user) => {
      const htmlContent = generateDataForNewConversation(user=user)
      newConversationUl.innerHTML += htmlContent;
    })
  } else {
    const htmlContent = generateDataForNewConversation()
    newConversationUl.innerHTML = htmlContent;
  }
};


newConversationInput.addEventListener("input", ()=>{
  if (newConversationInput.value) {
    newConversationSocket.send(
      JSON.stringify({"username": newConversationInput.value})
    );
  } else {
    toggleHiddeNewConversationDiv(needHide=true);
    modifyAvailableConversation(isNewConversation=false);
  }
});


function modifyAvailableConversation(isNewConversation) {
  if (isNewConversation) {
    availableConversation.classList.add("mt-3");
    availableConversation.style.height = "65%";
  } else {
    availableConversation.classList.remove("mt-3");
    availableConversation.style.height = "100%";
  }
}

function toggleHiddeNewConversationDiv(needHide) {
  if (needHide) {
    newConversationDiv.style.display = "none";
  } else {
    newConversationDiv.style.display = "block";
  }
}

function generateDataForNewConversation(user) {
  if (user) {
    return `
          <li>
            <div id="${user.fields.username}" class="d-flex bd-highlight">
              <div class="img_cont">
                <img src="" class="rounded-circle user_img">
                <span class="online_icon ${user.fields.is_online ? 'online' : 'offline'}"></span>
              </div>
              <div class="user_info">
                <span>${user.fields.username}</span>
                <p>${user.fields.is_online ? 'online': 'offline'}</p>
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
