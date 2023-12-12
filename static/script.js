async function processAnswer() {
    // Get the user's question
    var questionInput = document.getElementById('question');
    var question = questionInput.value.trim();

    // If the question is not empty, make an API request to get the answer
    if (question !== '') {
        // Create a new message element for the user's question
        var userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.innerText = 'You: \n' + question;

        // Append the user's question to the chat box
        document.getElementById('chat-box').appendChild(userMessage);

        // Clear the input box
        questionInput.value = '';

        // Make an asynchronous request to get the answer
        const response = await fetch('/get_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'question': question,
            }),
        });

        // Parse the JSON response
        const result = await response.json();

        // Get the answer from the response
        const answer = result.answer;

        // Create a new message element for the model's answer
        var modelMessage = document.createElement('div');
        modelMessage.classList.add('message', 'model-message');
        modelMessage.innerText = 'LaMini: \n' + answer;

        // Append the model's answer to the chat box
        document.getElementById('chat-box').appendChild(modelMessage);

        // Scroll the chat box to the bottom to show the latest messages
        document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
    }
}
