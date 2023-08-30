import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
    const full_name = useLocalStorage('full_name', '');
    const user_role = useLocalStorage('user_role', '');
    
    return { full_name, user_role };
});
