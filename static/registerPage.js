
const form = document.getElementById('register-form');
const status = document.getElementById('status');

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    event.target.reset();
    
    console.log(`Username: ${username}, Password: ${password}`);
    
    await RegisterService.getInstance().register(username, password);
});