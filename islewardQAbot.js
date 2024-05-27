// ==UserScript==
// @name         Isleward Wiki Q&A
// @namespace    Siege
// @version      0.7
// @description  Provides answers to questions using the Isleward Wiki and OpenAI API. The user will have to navigate the isleward wiki a few times and ask it questions to get it fully set up. In the way an AI works, you must feed it information and this is the only way to feed it this information at the moment since it stores the information in local_storage
// @match        https://wiki.isleward.com/*
// @match        https://play.isleward.com/*
// @grant        none
// ==/UserScript==

(function () {
  const apiKey = '';

  const localStorageKey = 'isleward-wiki-qa-data';

  let content = null;

  let trainingContent = '';

  let questionHistory = JSON.parse(localStorage.getItem(localStorageKey));

  // Check if questionHistory is an array, and if not, initialize it as an empty array
  if (!Array.isArray(questionHistory)) {
    questionHistory = [];
  }

  const consoleContainer = document.createElement('div');
  consoleContainer.classList.add('isleward-wiki-qa-console-container');
  consoleContainer.style.position = 'fixed';
  consoleContainer.style.bottom = '0';
  consoleContainer.style.right = '50%';
  consoleContainer.style.transform = 'translateX(50%)';
  consoleContainer.style.width = '300px';
  consoleContainer.style.backgroundColor = '#1a1a1a';
  consoleContainer.style.color = '#e0e0e0'; // Replace #333 with your desired text color
  consoleContainer.style.padding = '10px';
  consoleContainer.style.borderTop = '1px solid #333333';
  consoleContainer.style.boxShadow = '-2px 0px 10px rgba(0, 0, 0, 0.1)';
  consoleContainer.style.zIndex = '999999';
  consoleContainer.style.fontFamily = 'Arial, sans-serif';
  consoleContainer.style.cursor = 'grab'; // Set initial cursor as grab
  consoleContainer.style.maxHeight = '300px'; // Set the maximum height of the console
/*
  let isDragging = false;

let isScrolling = false; // Variable to keep track of scrolling

let dragOffsetX = 0;
let dragOffsetY = 0;

let prevX = 0;
let prevY = 0;
*/
const initialHeight = 300;
let consoleHeight = initialHeight;
/*
consoleContainer.style.height = `${consoleHeight}px`;

// Start dragging when the handle is clicked
const consoleHandle = document.createElement('div');
consoleHandle.style.width = '100%';
consoleHandle.style.height = '10px';
consoleHandle.style.cursor = 'grab';
consoleContainer.insertBefore(consoleHandle, consoleContainer.firstChild);

consoleHandle.addEventListener('mousedown', startDrag);

function startDrag(event) {
  isDragging = true;
  dragOffsetX = event.clientX - consoleContainer.offsetLeft;
  dragOffsetY = event.clientY - consoleContainer.offsetTop;

  prevX = event.clientX;
  prevY = event.clientY;

  document.addEventListener('mousemove', handleDrag);
  document.addEventListener('mouseup', endDrag);
}

function handleDrag(event) {
  if (isDragging) {
    const newX = event.clientX - dragOffsetX;
    const newY = event.clientY - dragOffsetY;

    const deltaX = newX - prevX;
    const deltaY = newY - prevY;

    prevX = newX;
    prevY = newY;

    const consoleWidth = consoleContainer.clientWidth;
    const maxWidth = window.innerWidth - consoleWidth;
    const maxHeight = window.innerHeight;

    const newLeft = Math.max(0, Math.min(newX, maxWidth));
    const newTop = Math.max(0, Math.min(newY, maxHeight - consoleHeight));

    consoleContainer.style.left = `${newLeft}px`;
    consoleContainer.style.top = `${newTop}px`;

    const newHeight = Math.min(consoleHeight + deltaY, maxHeight - newTop);
    consoleContainer.style.height = `${newHeight}px`;

    consoleHeight = newHeight;
  }
}

function endDrag() {
  isDragging = false;
  document.removeEventListener('mousemove', handleDrag);
  document.removeEventListener('mouseup', endDrag);
}
*/
consoleContainer.style.overflowY = 'auto';
consoleContainer.style.maxHeight = '300px';
// Create the consoleLogContainer and append consoleLog to it
const consoleLogContainer = document.createElement('div');
consoleLogContainer.style.overflowY = 'auto'; // Add this line to enable vertical scrollbar
consoleLogContainer.style.maxHeight = `${consoleHeight - 20}px`; // Adjust the value as needed

const consoleLog = document.createElement('div');
consoleLog.id = 'isleward-wiki-qa-console-log';

consoleLogContainer.appendChild(consoleLog); // Add the consoleLog to the container

const consoleInput = document.createElement('input'); // Create the consoleInput element
consoleInput.classList.add('isleward-wiki-qa-console-input');
consoleInput.placeholder = 'Ask a question or feed information to the AI...';
consoleInput.autocomplete = 'off';

consoleContainer.appendChild(consoleInput); // Append the consoleInput to the consoleContainer
consoleContainer.appendChild(consoleLogContainer); // Add the consoleLogContainer to the consoleContainer


consoleContainer.appendChild(consoleInput);
consoleContainer.appendChild(consoleLog);

  document.body.insertBefore(consoleContainer, document.body.firstChild);

  const aiInputElement = document.createElement('input');
  aiInputElement.classList.add('isleward-wiki-qa-console-input');
  aiInputElement.placeholder = 'Enter AI input...';
  aiInputElement.autocomplete = 'off';

  consoleContainer.insertBefore(aiInputElement, consoleInput);

  function scrapeWebpage() {
    const paragraphs = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6');
    const allElements = Array.from(paragraphs);
    const textContent = allElements.map(element => element.textContent.trim()).join('\n');
    return textContent;
  }

  async function generateAnswer(question, context) {
  const apiUrl = 'https://api.openai.com/v1/chat/completions';

  const messages = [
    { role: 'system', content: 'You are a helpful assistant that provides information from the Isleward Wiki.' },
    { role: 'user', content: question },
    { role: 'assistant', content: context }
  ];

  const requestBody = {
    messages,
    max_tokens: 100,
    temperature: 0.5,
    top_p: 1.0,
    n: 1,
    stop: '\n',
    model: 'gpt-3.5-turbo'
  };

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify(requestBody)
  });

  const data = await response.json();

  if (response.ok) {
    const answer = data.choices[0].message.content.trim();

    trainingContent += `\nQ: ${question}\nA: ${answer}`;

    if (!content) {
      content = scrapeWebpage();
      localStorage.setItem(localStorageKey, JSON.stringify(content));
    }

    return answer;
  } else {
    throw new Error(`Failed to generate answer: ${data.error.message}`);
  }
}

  function clearConsole() {
    consoleLog.innerHTML = '';
    consoleContainer.style.display = 'block';
  }

  window.clearConsole = clearConsole;

  consoleLog.addEventListener('click', async (event) => {
    if (event.target.classList.contains('isleward-wiki-qa-console-question')) {
      await handleQuestionClick(event);
    }
  });

  function scrollToBottom() {
    consoleLog.scrollTop = consoleLog.scrollHeight;
  }

consoleContainer.style.maxHeight = '300px'; // Adjust the value as needed

  function displayQuestionAnswer(question, answer) {
    const questionElement = document.createElement('p');
    questionElement.classList.add('isleward-wiki-qa-console-question');
    questionElement.textContent = `Q: ${question}`;
    questionElement.style.color = '#ff8800'; // Dark mode question text color

    const answerElement = document.createElement('div');
    answerElement.classList.add('isleward-wiki-qa-console-answer');
    answerElement.innerHTML = `<p>A: ${answer}</p>`;
    answerElement.style.color = '#00cc00'; // Dark mode answer text color

    consoleLog.appendChild(questionElement);
    consoleLog.appendChild(answerElement);

    // Automatically scroll to the bottom where the newest answered question is
    consoleLog.scrollTop = consoleLog.scrollHeight;
  }

async function handleUserInput() {
  const question = consoleInput.value.trim();
  if (question === '') return;

  consoleInput.value = '';

  const questionElement = document.createElement('p');
  questionElement.classList.add('isleward-wiki-qa-console-question');
  questionElement.textContent = `Q: ${question}`;
  consoleLog.appendChild(questionElement);

  try {
    if (!content) {
      content = scrapeWebpage();
    }

    const answer = await generateAnswer(question, content);

    displayQuestionAnswer(question, answer);

    questionHistory.push(question);
    localStorage.setItem(localStorageKey, JSON.stringify(questionHistory));

    sendMessage(answer);
  } catch (error) {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = `Error: ${error.message}`;
    consoleLog.appendChild(errorMessage);
  }

  consoleLog.scrollTop = consoleLog.scrollHeight;
  scrollToBottom();
}

  async function handleQuestionClick(event) {
  const question = event.target.textContent.slice(3);

  const questionElement = document.createElement('p');
  questionElement.classList.add('isleward-wiki-qa-console-question');
  questionElement.textContent = `Q: ${question}`;
  consoleLog.appendChild(questionElement);

  try {
    if (!content) {
      content = scrapeWebpage();
    }

    const answer = await generateAnswer(question, content);

    displayQuestionAnswer(question, answer);

    sendMessage(answer);
  } catch (error) {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = `Error: ${error.message}`;
    consoleLog.appendChild(errorMessage);
  }

  consoleLog.scrollTop = consoleLog.scrollHeight;
  scrollToBottom();
}

  consoleInput.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      await handleUserInput();
    }
  });

  aiInputElement.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      const aiInput = aiInputElement.value.trim();
      if (aiInput === '') return;

      aiInputElement.value = '';

      try {

        const answer = await generateAnswer(aiInput, '');

        displayQuestionAnswer(aiInput, answer);

        sendMessage(answer);
      } catch (error) {

        const errorMessage = document.createElement('p');
        errorMessage.textContent = `Error: ${error.message}`;
        consoleLog.appendChild(errorMessage);
      }

      consoleLog.scrollTop = consoleLog.scrollHeight;
    }
  });

  consoleLog.addEventListener('click', async (event) => {
    if (event.target.classList.contains('isleward-wiki-qa-console-question')) {
      await handleQuestionClick(event);
    }
  });
  document.body.insertBefore(consoleContainer, document.body.firstChild);

  questionHistory.forEach(question => {
    const questionElement = document.createElement('p');
    questionElement.classList.add('isleward-wiki-qa-console-question');
    questionElement.textContent = `Q: ${question}`;
    consoleLog.appendChild(questionElement);
  });

  function sendMessage(message) {
    const channel = getCurrentChannel();
    if (channel) {
      channel.sendMessage(message);
    }
  }

  function getCurrentChannel() {
    const channelList = window.isleward.chat.channels;
    const currentChannelId = window.isleward.chat.current;
    return channelList.find(channel => channel.id === currentChannelId);
  }

const originalSendMessage = window.isleward.chat.Channel.prototype.sendMessage;
window.isleward.chat.Channel.prototype.sendMessage = function (message) {

  originalSendMessage.apply(this, arguments);

  const isBotMessage = this.name === 'Wiki Q&A Bot';

  const messageElement = document.createElement('div');
  messageElement.classList.add('isleward-wiki-qa-console-answer');
  messageElement.innerHTML = `<p>${isBotMessage ? 'Bot' : 'You'}: ${message}</p>`;
  consoleLog.appendChild(messageElement);
}
  consoleLog.scrollTop = consoleLog.scrollHeight;
  scrollToBottom();
})();