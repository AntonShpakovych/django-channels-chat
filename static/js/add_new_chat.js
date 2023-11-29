function addNewChat(element){
    chatCreateSocket.send(JSON.stringify({"contact": element.id}))

    chatCreateSocket.onmessage = function (e){
        let status = JSON.parse(e.data).status;

        if (status === "CREATED") {
            chatListSocket.send(JSON.stringify({"type": "UPDATE"}))
        }
    }
    toggleHiddeNewContactsDiv(true);
    modifyAvailableChats(false);
}
