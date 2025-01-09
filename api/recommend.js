const express = require('express');
const app = express();
const path = require('path');

// Insert where items are collected
function grabRec(value) {
  let lst = value;
  // order list
  lst.sort((a, b) => a.age - b.age);
  // Input where items are split between their name, link, and number of searchs
  let result = [];
  for (let i = 0; i < 9; i++) {
    result.push(lst[i]);
  }
  return result;
};

var items = grabRec();
const markdownData = `
# Recommended Items

- **[Item 1](https://example.com/product1)**: 
- **[Item 2](https://example.com/service2)**: 
- **[Item 3](https://example.com/resource3)**: 

_Updated as of January 2025._
`;

app.get('/tri2/socialmedia_frontend/navigation/recommended.md', (req, res) => {
  res.send(markdownData);
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/script.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'script.js'));
});

const PORT = 4887;
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});