import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
    const full_name = ref('');
    const user_role = ref('');
    
    return { full_name, user_role };
});