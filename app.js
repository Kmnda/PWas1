// app.js
const http = require('http');

const hostname = '0.0.0.0'; // Listen on all available network interfaces
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello, World from my Node.js CI project!\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://<span class="math-inline">\{hostname\}\:</span>{port}/`);
  console.log('Hello, World from my Node.js CI project!'); // For Jenkins log
});

// Optional: Add a simple function that could be "tested"
function add(a, b) {
    return a + b;
}
console.log("Sum test: 2+3 =", add(2,3)); // For Jenkins log
