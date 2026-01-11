// C:\Users\Kartik\OneDrive\Desktop\chatbot2\static\script.js
// Initialize chat on page load
document.addEventListener('DOMContentLoaded', function() {
    // Display welcome message
    addBotMessage("Hello! I'm the SIES Nerul College Chatbot. How can I help you today?");
});

// Function to add bot message to chat
function addBotMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to add user message to chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send message to backend
async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message === '') return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input field
    userInput.value = '';
    
    // Send request to Flask backend at /get endpoint
    try {
        const response = await fetch('/get', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Add bot response to chat
        addBotMessage(data.reply);
    } catch (error) {
        addBotMessage("Sorry, I'm having trouble connecting to the server. Please try again later.");
        console.error('Error:', error);
    }
}

// Function to handle quick button clicks
function sendQuickMessage(message) {
    document.getElementById('user-input').value = message;
    sendMessage();
}

// Function to handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Add event listener for the send button
document.querySelector('.chat-input button').addEventListener('click', sendMessage);

// Focus the input field when page loads
document.getElementById('user-input').focus();