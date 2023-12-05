const findNewContactInput = document.getElementById("find-new-contacts").querySelector("input");
const newContactsDiv = document.getElementById("new-contacts");
const newContactsUl = newContactsDiv.querySelector("ul");
const availableChats = document.getElementById("available-chats");
const availableChatsUl = availableChats.querySelector("ul");
const chatHeaderDiv = document.getElementById("chat-header");
const chatHeaderSpan = chatHeaderDiv.querySelector("span");
const chatHeaderP = chatHeaderDiv.querySelector("p");
const chatHistoryDiv = document.getElementById("chat-history");
const currentUserUsername = JSON.parse(document.getElementById("current-user-username").textContent);
const chatMessageInput = document.getElementById("chat-message-input");
const chatMessageSubmit = document.getElementById("chat-message-submit");

const findNewContactsSocket = new WebSocket(`ws://${window.location.host}/ws/contacts/find/new/`);
const chatListSocket = new WebSocket(`ws://${window.location.host}/ws/chats/`);
const chatCreateSocket = new WebSocket(`ws://${window.location.host}/ws/chats/new/`);
