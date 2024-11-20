async function loadChat() {
    let roomName = document.getElementById("room-name-input").value
    await loadPage("/chat/" + roomName + "/")
    addHistory("/chat/" + roomName + "/")
    await chatSocket()
}

async function chatSocket() {
    console.log("chatSocket lance")
        // Variables pour le chat public
        const username = "{{user.username}}";
        const roomName = "example_room";
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/' + roomName + '/'
        );

        // Variables pour le chat privé
        const privateChatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/private_chat/'
        );

        // Quand un message public est reçu
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data);
            const chatLog = document.querySelector('#chat-log');
            chatLog.value += '[Public] ' + data.username + ': ' + data.message + '\n';
            console.log(data.username);
            chatLog.scrollTop = chatLog.scrollHeight;
        };

        // Quand un message privé est reçu
        privateChatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const chatLog = document.querySelector('#chat-log');
            chatLog.value += '[Privé de ' + data.sender + '] : ' + data.message + '\n';
            chatLog.scrollTop = chatLog.scrollHeight;
        };

        // Fermeture des WebSockets
        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
        privateChatSocket.onclose = function(e) {
            console.error('Private chat socket closed unexpectedly');
        };

        // Afficher ou masquer la zone du destinataire en fonction du type de message
        document.getElementById('message-type').onchange = function(e) {
            const recipientInput = document.querySelector('#recipient-input');
            if (this.value === 'private') {
                recipientInput.style.display = 'block'; // Montrer la zone pour le destinataire
            } else {
                recipientInput.style.display = 'none'; // Cacher la zone pour le destinataire
            }
        };

        // Envoi de message (public ou privé) lorsque le bouton est cliqué
        document.getElementById('message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#message-input');
            const message = messageInputDom.value.trim();
            const messageType = document.querySelector('#message-type').value;
            const recipientInputDom = document.querySelector('#recipient-input');
            const recipient = recipientInputDom.value.trim();

            if (message) {
                if (messageType === 'public') {
                    // Envoyer un message public
                    chatSocket.send(JSON.stringify({
                        'message': message,
                        'username': username, // Remplace par le nom d'utilisateur
                    }));
                } else if (messageType === 'private' && recipient) {
                    // Envoyer un message privé
                    privateChatSocket.send(JSON.stringify({
                        'message': message,
                        'recipient': recipient
                    }));
                }
                // Réinitialiser les champs de message
                messageInputDom.value = '';
                recipientInputDom.value = '';
            }
        };
}