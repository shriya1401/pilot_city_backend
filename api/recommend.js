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

- **[${items[1].name}](${items[1].link})**: 
- **[${items[2].name}](${items[2].link})**: 
- **[${items[3].name}](${items[3].link})**: 

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