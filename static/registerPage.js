
const form = document.getElementById('login-form');
const status = document.getElementById('status');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    event.target.reset();
    
    console.log(`Username: ${username}, Password: ${password}`);
    dataInsert(username, password);
});