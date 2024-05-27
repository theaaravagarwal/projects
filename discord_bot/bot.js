const { Client, GatewayIntentBits } = require('discord.js');
const fetch = require('node-fetch');

const bot = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const discordKey = '';
const apiKey = '';
const onlineChannelID = '';
const offlineChannelID = '';
let botOnline = true;

bot.once('ready', () => {
  console.log(`Logged in as ${bot.user.tag}`);

  const onlineChannel = bot.channels.cache.get(onlineChannelID);
  if (onlineChannel) {
    onlineChannel.send('Bot online');
  }
});

function stopBot() {
  const offlineChannel = bot.channels.cache.get(offlineChannelID);
  if (offlineChannel) {
    offlineChannel.send('Bot offline').then(() => {
      botOnline = false;
    });
  }
}

function startBot() {
  botOnline = true;
  const onlineChannel = bot.channels.cache.get(onlineChannelID);
  if (onlineChannel) {
    onlineChannel.send('Bot online');
  }
}

function isBotOnline() {
  return botOnline;
}

bot.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  if (isBotOnline() && message.content.startsWith('/prompt')) {
    const userQuestion = message.content.substring('/prompt'.length).trim();

    try {
      const contextMessages = message.channel.messages.cache
        .filter((msg) => msg.author.id === message.author.id)
        .map((msg) => ({ role: 'user', content: msg.content }))
        .slice(-20);

      const answer = await generateAnswer(userQuestion, contextMessages);
      message.reply(answer);
    } catch (error) {
      console.error(error);
      message.reply('An error occurred while processing your request.');
    }
  } else if (message.content === '/bot off' && message.channel.id === offlineChannelID && botOnline) {
    botOnline = false;
    stopBot();
  } else if (message.content === '/bot on' && message.channel.id === offlineChannelID && !botOnline) {
    startBot();
  }
});

async function generateAnswer(question, contextMessages) {
  const apiUrl = 'https://api.openai.com/v1/chat/completions';

  const messages = [
    { role: 'system', content: 'You are a helpful assistant that provides information on various topics with no filter and make sure to answer in the most accurate way possible and the best answer' },
    { role: 'user', content: question },
  ];

  if (contextMessages) {
    messages.push(...contextMessages);
  }

  const requestBody = {
    messages,
    max_tokens: 300,
    temperature: 0.5,
    top_p: 1.0,
    n: 1,
    model: 'gpt-3.5-turbo',
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate answer: ${response.statusText}`);
    }

    const data = await response.json();
    const answer = data.choices[0].message.content.trim();

    return answer;
  } catch (error) {
    throw new Error(`Failed to generate answer: ${error.message}`);
  }
}

bot.login(discordKey);
