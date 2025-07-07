function appendMessage(sender, text) {
  const box = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.className = sender + '-message';
  div.innerHTML = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function sendMessage() {
  const inp = document.getElementById('user-input');
  const raw = inp.value.trim();
  if (!raw) return;
  appendMessage('user', raw);
  inp.value = '';

  const msg = raw.toLowerCase();
  let reply = '';

  if (msg.includes('hi') || msg.includes('hello')) {
    reply = 'Hello! How may I help you?';
  } else if (msg.includes('job') || msg.includes('vacancy')) {
    reply = `
      We have job categories:<br>
      🔧 <a href="/jobs/tech">Tech</a><br>
      🧾 <a href="/jobs/non-tech">Non‑Tech</a><br>
      🧩 <a href="/jobs/other">Other</a>
    `;
  } else {
    reply = "Sorry, I don't understand. Please ask about jobs.";
  }

  setTimeout(() => appendMessage('bot', reply), 200);
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('user-input')
    .addEventListener('keydown', e => e.key === 'Enter' && sendMessage());
  document.querySelector('.input-area button')
    .addEventListener('click', sendMessage);
});
