
class EnvVariablesService {

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!EnvVariablesService.#_instance) {
            EnvVariablesService.#_instance = new EnvVariablesService()
        }
        return EnvVariablesService.#_instance
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
