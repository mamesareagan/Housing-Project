// script.js
// This script is optional if you're okay with using CSS for hover effect
// You can use this script if you need to support older browsers that don't handle hover events well with CSS alone

document.querySelector('.dropdown').addEventListener('mouseenter', function() {
    document.querySelector('.dropdown-content').style.display = 'block';
});

document.querySelector('.dropdown').addEventListener('mouseleave', function() {
    document.querySelector('.dropdown-content').style.display = 'none';
});
