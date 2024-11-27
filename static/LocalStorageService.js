

class LocalStorageService {

    // private fields start with #
    static #_instance

    static getInstance(){
        if(!LocalStorageService.#_instance) {
            LocalStorageService.#_instance = new LocalStorageService()
        }
        return LocalStorageService.#_instance
    }

    setItem(key, value) {
        localStorage.setItem(key, JSON.stringify(value))
    }
    
    getItem(key) {
        const data = localStorage.getItem(key)
        return JSON.parse(data)
    }
}