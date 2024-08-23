document.addEventListener('DOMContentLoaded', () => {
    // Get the form elements
    const form = document.querySelector('#message-form');
    const occasionSelect = document.querySelector('#occasion');
    const messageTextarea = document.querySelector('#message');
    const senderNameInput = document.querySelector('#sender-name');
    const recipientNameInput = document.querySelector('#recipient-name');
    const countryCodeInput = document.querySelector('#country-code');
    const recipientNumberInput = document.querySelector('#recipient-number');
    const scheduleDateInput = document.querySelector('#schedule-date');
    const scheduleTimeInput = document.querySelector('#schedule-time');
    const messageTypeSelect = document.querySelector('#message-type');
    const sendButton = document.querySelector('#send-button'); // Combined button

    // Add event listener to the form
    form.addEventListener('submit', handleFormSubmit);

    function handleFormSubmit(event) {
        event.preventDefault();

        const occasion = occasionSelect.value;
        const message = messageTextarea.value;
        const senderName = senderNameInput.value;
        const recipientName = recipientNameInput.value;
        const countryCode = countryCodeInput.value;
        const recipientNumber = recipientNumberInput.value;
        const scheduleDate = scheduleDateInput.value;
        const scheduleTime = scheduleTimeInput.value;
        const messageType = messageTypeSelect.value;

        if (!occasion || !message || !scheduleDate || !scheduleTime) {
            alert('Please fill in all required fields.');
            return;
        }

        if (messageType === 'whatsapp' && !recipientNumber) {
            alert('Please provide a WhatsApp number.');
            return;
        }

        if (messageType === 'sms' && !recipientNumber) {
            alert('Please provide a phone number.');
            return;
        }

        const fullNumber = countryCode + recipientNumber;

        const payload = {
            occasion: occasion,
            message: message,
            senderName: senderName,
            recipientName: recipientName,
            recipientNumber: fullNumber,
            scheduleDate: scheduleDate,
            scheduleTime: scheduleTime,
            messageType: messageType
        };

        fetch('/schedule_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Message scheduled successfully!');
            } else {
                alert('Failed to schedule message: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error scheduling message');
        });
    }
});
