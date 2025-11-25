let socket = io();
let username = "";
let room = "";

function joinRoom() {
    username = document.getElementById("username").value;
    room = document.getElementById("room").value;

    socket.emit("join", { username, room });
}

socket.on("chat_history", (messages) => {
    const chat = document.getElementById("chat");
    chat.innerHTML = "";
    messages.forEach(msg => {
        chat.innerHTML += msg + "<br>";
    });
});

socket.on("message", (msg) => {
    const chat = document.getElementById("chat");
    chat.innerHTML += msg + "<br>";
    chat.scrollTop = chat.scrollHeight;
});

function sendMsg() {
    let text = document.getElementById("msgBox").value;
    socket.emit("message", { username, room, msg: text });
    document.getElementById("msgBox").value = "";
}
