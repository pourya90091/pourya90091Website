var showdown  = require('showdown'),
    converter = new showdown.Converter()

const md_viewer = document.getElementById('md-viewer');
const content = document.getElementById('id_content');

md_viewer.innerHTML = converter.makeHtml(content.value) // in case of first loading of the page

content.addEventListener('keydown', function() {
    md_viewer.innerHTML = converter.makeHtml(content.value)
});

content.addEventListener('keyup', function() {
    md_viewer.innerHTML = converter.makeHtml(content.value)
});
