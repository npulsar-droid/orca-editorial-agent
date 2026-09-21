const { marked } = require('marked');
console.log(marked.parse('|a|b|\n|---|---|\n|c|d|'));
