//Cretae function for validating forms
function validateForm(event) {
    const form = event.target; // Get the form being submitted
    const fields = form.querySelectorAll('input[type="text"], input[type="number"]'); // Adjust selector based on your form structure
    let isValid = true;

    fields.forEach(field => {
        const value = field.value;
        if (!isValidNumber(value) && value !== '') {
            isValid = false; // Mark as invalid
            alert(`${field.name} field accepts (numbers, decimal) only.`); // Show alert for invalid field
            field.focus(); // Optional: Set focus back to the invalid field
            return; // Stop checking after finding the first invalid field
        }
    });

    if (!isValid) {
        event.preventDefault(); // Prevent form submission if any field is invalid
    }
}

// Map a field to its message_field
const message_fields_map = {
    "potassium": "k",
    "phosphorus": "p",
    "ph": "_ph",
    "nitrogen": "n",
    "rainfall": "_rain",
    "humidity": "_hum",
    "temperature": "_temp"
};

// Map a field to its message
const message_map = {
    "k": "Potassium field accepts (numbers, decimal) only.",
    "p": "Phosphorus field accepts (numbers, decimal) only.",
    "n": "Nitrogen field accepts (numbers, decimal) only.",
    "_ph": "PH field accepts (numbers, decimal) only.",
    "_rain": "Rainfall field accepts (numbers, decimal) only.",
    "_hum": "Humidity field accepts (numbers, decimal) only.",
    "_temp": "Temperature field accepts (numbers, decimal) only."
};

// Message queue
let messageQueue = [];
let isProcessing = false;

function InputEventListener() {
    const fields = document.querySelectorAll('#potassium, #phosphorus, #nitrogen, #ph, #rainfall, #humidity, #temperature');

    fields.forEach(element => {
        element.addEventListener('input', handleInputEvent); // Attach the event listener
    });
}

function handleInputEvent(event) {
    const fieldName = event.target.name;
    const message_field = message_fields_map[fieldName];

    if (!message_field) return; // If the field doesn't exist in the map, do nothing

    const value = event.target.value;

    // Find the form containing the input
    const form = event.target.closest('form');
    if (!form) return;

    // Find the specific message element within the correct form
    const messageElement = form.querySelector(`#${message_field}`);

    if (!messageElement) return; // If the message element doesn't exist, exit

    if (value === '') {
        // If value is empty, clear the message
        enqueueMessage('', messageElement);
    } else {
        const isValid = isValidNumber(value);
        if (!isValid) {
            const message = message_map[message_field];
            // Check if the message element is already populated
            if (messageElement.innerHTML === '') {
                enqueueMessage(message, messageElement); // Enqueue message to be displayed if no existing text
            }
        } else {
            // If valid, clear the message
            enqueueMessage('', messageElement);
        }
    }
}

function enqueueMessage(message, element) {
    messageQueue.push({ message, element });
    processQueue();
}

function processQueue() {
    if (isProcessing || messageQueue.length === 0) return; // Exit if already processing or no messages

    isProcessing = true; // Mark as processing
    const { message, element } = messageQueue.shift(); // Get the next message from the queue

    // Start typing effect based on the message content
    if (message === '') {
        clearMessage(element, () => {
            isProcessing = false; // Finished processing, allow next
            processQueue(); // Continue with the next in queue
        });
    } else {
        // If there is already text, do not type the message
        if (element.innerHTML !== '') {
            isProcessing = false; // Reset processing since we won't type
            return; // Skip typing if there's already a message
        }
        typeMessage(message, element, () => {
            isProcessing = false; // Finished processing, allow next
            processQueue(); // Continue with the next in queue
        });
    }
}

function typeMessage(message, element, callback) {
    let index = 0; // Reset index for typing

    function type() {
        if (index < message.length) {
            element.innerHTML += message.charAt(index);
            index++;
            setTimeout(type, 20); // Typing effect
        } else {
            callback(); // Call the callback when done typing
        }
    }
    type(); // Start the typing effect
}

function clearMessage(element, callback) {
    let index = element.innerHTML.length; // Start from the current length

    function clear() {
        if (index > 0) {
            element.innerHTML = element.innerHTML.slice(0, -1); // Remove last character
            index--;
            setTimeout(clear, 20); // Typing effect for clearing
        } else {
            callback(); // Call the callback when done clearing
        }
    }
    clear(); // Start the clearing effect
}

function isValidNumber(value) {
    const regex = /^\d+(\.\d+)?$/;
    return regex.test(value);
}

// Initialize event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', InputEventListener);
