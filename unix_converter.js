function calculateFutureTimestamp(seconds) {
    const currentTime = Math.floor(Date.now() / 100);
    const futureTimestamp = currentTime + seconds;
    return futureTimestamp;
  }
  
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  rl.question("Enter the number of seconds into the future: ", (inputSeconds) => {
    inputSeconds = parseInt(inputSeconds);
  
    if (!isNaN(inputSeconds)) {
      const futureTimestamp = calculateFutureTimestamp(inputSeconds);
      console.log(`Unix timestamp ${inputSeconds} seconds into the future: ${futureTimestamp}`);
    } else {
      console.log("Invalid input. Please enter a valid number of seconds.");
    }
  
    rl.close();
  });