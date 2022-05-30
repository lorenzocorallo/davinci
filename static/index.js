const messages = document.querySelector("#messages");

const getCurrentTime = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });


const onUpdate = () => {
    messages.scrollTop = messages.scrollHeight;
    document.querySelector("#msg-input").focus();
};

const addTypingMsg = (sender) => {
    const msg = document.createElement('div');
    msg.classList.add('msg');
    msg.dataset["sender"] = "bot";
    const msgContent = document.createElement('p');
    msgContent.classList.add('msg-content');
    const msgSender = document.createElement('span');
    msgSender.classList.add('msg-sender');
    msgSender.innerText = sender;
    const msgTimestamp = document.createElement('span');
    msgTimestamp.classList.add('msg-timestamp');
    msgTimestamp.innerText = getCurrentTime();

    const typing = document.createElement('div');
    typing.classList.add('typing');
    const dot = document.createElement('span');
    dot.classList.add('dot');
    typing.appendChild(dot);
    typing.appendChild(dot.cloneNode());
    typing.appendChild(dot.cloneNode());

    msg.appendChild(msgTimestamp);
    msg.appendChild(msgSender);
    msg.appendChild(msgContent);
    msgContent.appendChild(typing);
    const el = messages.appendChild(msg);
    onUpdate();
    return el;
};

const makeMsg = (content, sender, timestamp, is_bot = false) => {
    const msg = document.createElement('div');
    msg.classList.add('msg');
    msg.dataset["sender"] = is_bot ? "bot" : "sender";
    const msgContent = document.createElement('p');
    msgContent.classList.add('msg-content');
    msgContent.innerText = content;
    const msgSender = document.createElement('span');
    msgSender.classList.add('msg-sender');
    msgSender.innerText = sender;
    const msgTimestamp = document.createElement('span');
    msgTimestamp.classList.add('msg-timestamp');
    msgTimestamp.innerText = timestamp;
    msg.appendChild(msgTimestamp);
    msg.appendChild(msgSender);
    msg.appendChild(msgContent);
    const el = messages.appendChild(msg);
    onUpdate();
    return el;
};

let ai_username;
const sessionInfo = document.querySelector("#session-info");
const restoreOrInitSession = async () => {
    ai_username = new URLSearchParams(window.location.search).get('ai_username');

    const dialog = await fetch('/dialog').then(res => res.json()).then(obj => obj.dialog);
    if (!dialog || dialog.length == 0) {
        sessionInfo.innerText = `Nuova sessione, ${ai_username}.`;
        return makeMsg(`Ciao, sei in contatto con ${ai_username} invia il primo messaggio`, "DaVinci", getCurrentTime(), true);
    }
    sessionInfo.innerText = `Sessione ripristinata, ${ai_username}, iniziata alle ${dialog[0].timestamp}.`;
    dialog.map(msg => {
        makeMsg(msg.content, msg.sender, msg.timestamp, msg.sender.toLowerCase() != "tu");
    });
};

document.addEventListener("DOMContentLoaded", function () {
    restoreOrInitSession();
});

const form = document.querySelector("#msg-form");
const msgInput = document.querySelector("#msg-input");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msgContent = msgInput.value;
    if (msgContent.length == 0) return;
    makeMsg(msgContent, "Tu", getCurrentTime());
    msgInput.value = "";
    // wait 0.4s
    await new Promise(resolve => setTimeout(resolve, 400));
    const typingMsg = addTypingMsg(ai_username);
    const message = await fetch("/send", {
        method: "POST",
        body: JSON.stringify({ question: msgContent }),
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then(res => res.json()).then(obj => obj.message);
    typingMsg.querySelector(".typing").remove();
    typingMsg.querySelector(".msg-content").innerText = message.content;
    typingMsg.querySelector(".msg-timestamp").innerText = message.timestamp;
});
