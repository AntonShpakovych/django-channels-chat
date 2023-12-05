chatListSocket.onopen = function() {
  chatListSocket.send(JSON.stringify({"type": "GET"}));
}

chatListSocket.onmessage = function(e) {
  const chats = JSON.parse(e.data).chats;
  availableChatsUl.innerHTML = "";

  if (chats.length) {
    chats.forEach((chat) => {
      const htmlContent = generateItem(chat)
      availableChatsUl.innerHTML += htmlContent;
    })
  } else {
    const htmlContent = generateItem()
    availableChatsUl.innerHTML = htmlContent;
  }
};
