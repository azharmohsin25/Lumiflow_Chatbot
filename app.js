(() => {
  const config = window.__CHAT_CONFIG__ || {};
  const chatLog = document.getElementById("chatLog");
  const suggestions = document.getElementById("suggestions");
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const sendButton = chatForm?.querySelector(".send-btn");
  const scrollButton = document.querySelector("[data-scroll-to-chat]");
  const sampleButton = document.querySelector("[data-ask-prompt]");

  if (!chatLog || !suggestions || !chatForm || !chatInput || !sendButton) {
    return;
  }

  const fallbackPrompts = Array.isArray(config.starterPrompts) ? config.starterPrompts : [];
  const state = {
    typingNode: null,
    busy: false,
  };

  function scrollToBottom() {
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function createMessageElement(role, text, meta = []) {
    const article = document.createElement("article");
    article.className = `message message--${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message__avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = role === "user" ? "You" : "LF";

    const bubble = document.createElement("div");
    bubble.className = "message__bubble";

    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    bubble.appendChild(paragraph);

    if (meta.length > 0) {
      const metaRow = document.createElement("div");
      metaRow.className = "message__meta";

      meta.forEach((item) => {
        const span = document.createElement("span");
        span.textContent = item;
        metaRow.appendChild(span);
      });

      bubble.appendChild(metaRow);
    }

    article.appendChild(avatar);
    article.appendChild(bubble);
    return article;
  }

  function createTypingElement() {
    const article = document.createElement("article");
    article.className = "message message--bot message--typing";

    const avatar = document.createElement("div");
    avatar.className = "message__avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "LF";

    const bubble = document.createElement("div");
    bubble.className = "message__bubble";

    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.setAttribute("aria-label", "Assistant is typing");
    dots.innerHTML = "<span></span><span></span><span></span>";

    bubble.appendChild(dots);
    article.appendChild(avatar);
    article.appendChild(bubble);
    return article;
  }

  function setBusy(isBusy) {
    state.busy = isBusy;
    chatInput.disabled = isBusy;
    sendButton.disabled = isBusy;
    sendButton.textContent = isBusy ? "Thinking..." : "Send";
  }

  function clearTyping() {
    if (state.typingNode) {
      state.typingNode.remove();
      state.typingNode = null;
    }
  }

  function renderSuggestions(items) {
    suggestions.innerHTML = "";

    const chips = (Array.isArray(items) && items.length > 0 ? items : fallbackPrompts).slice(0, 4);
    chips.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "suggestion-chip";

      const title = document.createElement("span");
      title.textContent = item.category || "Prompt";

      const question = document.createElement("strong");
      question.textContent = item.question || item;

      button.appendChild(title);
      button.appendChild(question);
      button.addEventListener("click", () => {
        chatInput.value = question.textContent || "";
        chatInput.focus();
        void submitMessage(question.textContent || "");
      });

      suggestions.appendChild(button);
    });
  }

  function appendUserMessage(text) {
    chatLog.appendChild(createMessageElement("user", text));
    scrollToBottom();
  }

  function appendBotMessage(payload) {
    const meta = [];

    if (payload.match) {
      meta.push(`Best match: ${payload.match}`);
    }
    if (typeof payload.confidence === "number") {
      meta.push(`Confidence: ${payload.confidence}%`);
    }
    if (payload.reason) {
      meta.push(payload.reason);
    }

    chatLog.appendChild(createMessageElement("bot", payload.reply, meta));
    scrollToBottom();
  }

  async function submitMessage(rawText) {
    const text = (rawText ?? chatInput.value).trim();

    if (!text || state.busy) {
      if (!text) {
        chatInput.classList.add("is-invalid");
        window.setTimeout(() => chatInput.classList.remove("is-invalid"), 420);
      }
      return;
    }

    appendUserMessage(text);
    chatInput.value = "";
    chatInput.focus();
    clearTyping();
    state.typingNode = createTypingElement();
    chatLog.appendChild(state.typingNode);
    scrollToBottom();
    setBusy(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();
      clearTyping();
      appendBotMessage(data);
      renderSuggestions(data.suggestions);
    } catch (error) {
      clearTyping();
      appendBotMessage({
        reply:
          "I ran into a connection issue while looking that up. Please try again in a moment, or tap one of the sample prompts.",
        match: "Network error",
        confidence: 0,
        reason: "The request could not reach the FAQ service.",
      });
      renderSuggestions(fallbackPrompts);
      console.error(error);
    } finally {
      setBusy(false);
      scrollToBottom();
    }
  }

  chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    void submitMessage();
  });

  if (scrollButton) {
    scrollButton.addEventListener("click", () => {
      chatInput.scrollIntoView({ behavior: "smooth", block: "center" });
      chatInput.focus({ preventScroll: true });
    });
  }

  if (sampleButton) {
    sampleButton.addEventListener("click", () => {
      const prompt = sampleButton.getAttribute("data-ask-prompt") || fallbackPrompts[0] || "";
      chatInput.value = prompt;
      chatInput.focus();
      void submitMessage(prompt);
    });
  }

  chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void submitMessage();
    }
  });

  renderSuggestions(fallbackPrompts);
  scrollToBottom();
})();
