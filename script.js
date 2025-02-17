const SENTENCES = [
    "will you be my girlfirend",
    "will you be my valentine",
    "you are the love of my life",
    "my brother in atlantic city",
    "ehi is the best girlfriend"
  ];
  
  let sentence = [];
  let attempts = 6;
  let currentAttempt = 0;
  
  const board = document.getElementById("board");
  const guessInput = document.getElementById("guess-input");
  const submitButton = document.getElementById("submit-guess");
  const message = document.getElementById("message");
  
  // Initialize the game
  function init() {
    sentence = chooseSentence().split(" ");
    renderBoard();
  }
  
  // Choose a random sentence
  function chooseSentence() {
    return SENTENCES[Math.floor(Math.random() * SENTENCES.length)];
  }
  
  // Render the game board
  function renderBoard() {
    board.innerHTML = "";
    for (let i = 0; i < attempts; i++) {
      const row = document.createElement("div");
      row.className = "row";
      for (let j = 0; j < sentence.length; j++) {
        const cell = document.createElement("div");
        cell.className = "cell";
        row.appendChild(cell);
      }
      board.appendChild(row);
    }
  }
  
  // Check the guess and update the board
  function checkGuess(guess) {
    const words = guess.toLowerCase().split(" ");
    if (words.length !== sentence.length) {
      message.textContent = `Please enter exactly ${sentence.length} words.`;
      return;
    }
  
    const row = board.children[currentAttempt];
    let correctCount = 0;
  
    for (let i = 0; i < words.length; i++) {
      const cell = row.children[i];
      cell.textContent = words[i];
  
      if (words[i] === sentence[i]) {
        cell.classList.add("green");
        correctCount++;
      } else if (sentence.includes(words[i])) {
        cell.classList.add("yellow");
      } else {
        cell.classList.add("gray");
      }
    }
  
    if (correctCount === sentence.length) {
      message.textContent = "Congratulations! You guessed the sentence!";
      submitButton.disabled = true;
    } else {
      currentAttempt++;
      if (currentAttempt === attempts) {
        message.textContent = `Game over! The sentence was: ${sentence.join(" ")}`;
        submitButton.disabled = true;
      }
    }
  }
  
  // Event listener for the submit button
  submitButton.addEventListener("click", () => {
    const guess = guessInput.value.trim();
    if (guess) {
      checkGuess(guess);
      guessInput.value = "";
    }
  });
  
  // Initialize the game when the page loads
  init();