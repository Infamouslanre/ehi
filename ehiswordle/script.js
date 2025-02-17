const SENTENCES = [
    "will you be my girlfriend",
    "will you be my valentine",
    "you're the love of my life",
    "my brother in atlantic city",
    "ehi is the best girlfriend",
    "ehi has the best style",
    "ehi is gorgeous",
    "ehi is smart"
  ];
  
  let sentence = [];
  let attempts = 6;
  let currentAttempt = 0;
  
  const board = document.getElementById("board");
  const guessInput = document.getElementById("guess-input");
  const submitButton = document.getElementById("submit-guess");
  const restartButton = document.getElementById("restart-button");
  const message = document.getElementById("message");
  
  // Initialize the game
  function init() {
    sentence = chooseSentence().split(" ");
    currentAttempt = 0;
    renderBoard();
    guessInput.disabled = false;
    submitButton.disabled = false;
    restartButton.style.display = "none";
    message.textContent = "";
    guessInput.value = "";
    guessInput.focus(); // Focus the input for better mobile experience
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
      endGame();
    } else {
      currentAttempt++;
      if (currentAttempt === attempts) {
        message.textContent = `Game over! The sentence was: ${sentence.join(" ")}`;
        endGame();
      }
    }
  }
  
  // End the game (win or lose)
  function endGame() {
    guessInput.disabled = true;
    submitButton.disabled = true;
    restartButton.style.display = "block";
  }
  
  // Event listener for the submit button
  submitButton.addEventListener("click", () => {
    const guess = guessInput.value.trim();
    if (guess) {
      checkGuess(guess);
      guessInput.value = "";
    }
  });
  
  // Event listener for the Enter key
  guessInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      const guess = guessInput.value.trim();
      if (guess) {
        checkGuess(guess);
        guessInput.value = "";
      }
    }
  });
  
  // Event listener for the restart button
  restartButton.addEventListener("click", () => {
    init();
  });
  
  // Initialize the game when the page loads
  init();