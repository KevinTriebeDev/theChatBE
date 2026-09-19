const form = document.querySelector("#chat-form");
const chats = document.querySelector("#chats");
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

async function chatsLaden() {
    const response = await fetch("/api/chat/");
    const daten = await response.json();

    chats.innerHTML = daten.map(chat => `
        <p>
            <strong>${chat.name}</strong>: ${chat.message}
        </p>
    `).join("");
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    await fetch("/api/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            name: document.querySelector("#name").value,
            message: document.querySelector("#message").value
        })
    });

    form.reset();
    chatsLaden();
});

chatsLaden();