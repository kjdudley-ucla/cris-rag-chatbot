document.addEventListener("DOMContentLoaded", function() {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");

    function sendMessage() {
        const userMessage = userInput.value;
        if (!userMessage.trim()) return;
        
        // Create user message element
        const userMessageElement = document.createElement("div");
        userMessageElement.className = "message user-message";
        userMessageElement.textContent = "You: " + userMessage;
        chatBox.appendChild(userMessageElement);
        
        userInput.value = "";

        // Show loading indicator
        const loadingElement = document.createElement("div");
        loadingElement.className = "message bot-message loading";
        loadingElement.textContent = "Bot: Thinking...";
        chatBox.appendChild(loadingElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Updated endpoint to match our new blueprint structure
        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatBox.removeChild(loadingElement);
            
            // Create bot message element
            const botMessageElement = document.createElement("div");
            botMessageElement.className = "message bot-message";
            
            // Add prefix and sanitized HTML content
            const prefix = document.createElement("span");
            prefix.className = "message-prefix";
            prefix.textContent = "Bot: ";
            botMessageElement.appendChild(prefix);
            
            const content = document.createElement("div");
            content.className = "message-content";
            content.innerHTML = DOMPurify.sanitize(data.response);
            botMessageElement.appendChild(content);
            
            chatBox.appendChild(botMessageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            // Remove loading indicator
            chatBox.removeChild(loadingElement);
            
            console.error("Error:", error);
            const errorElement = document.createElement("div");
            errorElement.className = "message error-message";
            errorElement.textContent = "Bot: Sorry, something went wrong.";
            chatBox.appendChild(errorElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }

    // Add click event listener to send button
    sendButton.addEventListener("click", sendMessage);

    // Add enter key event listener to input field
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});