function chatDetail(element) {
  const chatDetailSocket = new WebSocket(`ws://${window.location.host}/ws/chats/${element.id}/`)

  chatDetailSocket.onmessage = function (e){
    const data = JSON.parse(e.data)

    if (data.hasOwnProperty("type") && data["type"] === "chat.message") {
      const message = functionGenerateMessage(data, data.user === currentUserUsername)
      updateQuantity()
      chatHistoryDiv.innerHTML += message
    } else {
      generateChatDetail(data)
    }
  }

  chatMessageInput.focus();
  chatMessageInput.onkeyup = function (e){
    if (e.key === "Enter") {
      chatMessageSubmit.click()
    }
  };

  chatMessageSubmit.onclick = function (e) {
    const message = chatMessageInput.value;

    chatDetailSocket.send(JSON.stringify({"message": message}))

    chatMessageInput.value = "";
  };
}
