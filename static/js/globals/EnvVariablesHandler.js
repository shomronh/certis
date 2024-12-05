
class EnvVariablesHandler {

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!EnvVariablesHandler.#_instance) {
            EnvVariablesHandler.#_instance = new EnvVariablesHandler()
        }
        return EnvVariablesHandler.#_instance
    }

    get backendUrl(){
        const key = "BACKEND_URL"
        const value = LocalStorageService.getInstance().getItem(key)
        if(value) return value
        throw new Error("BACKEND_URL env variable hasnt been initialized")
    }

    set backendUrl(value){
        const key = "BACKEND_URL"
        LocalStorageService.getInstance().setItem(key, value)
    }
}
