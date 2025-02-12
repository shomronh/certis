

const googleButton = document.getElementById('google_login_button')

    const loginService = LoginService.getInstance()
    
    loginService.showGoogleButton()
    
    // googleButton.addEventListener('click', async () => {
    //     await loginService.loginWithGoogle()
    // })