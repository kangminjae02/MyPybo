import { writable } from "svelte/store"


const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

// Global
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)

// Home
export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")

// etc...
export const UNKNOWN_ID = 9223372036854775807
export const UNKNOWN_USERNAME = 'UNKNOWN'
export const UNKNOWN_PASSWORD = 'alsaslfjqpoiefqdcv09120730151'