import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
    const id = useLocalStorage('id', '');
    const student_number = useLocalStorage('student_number', '');

    const full_name = useLocalStorage('full_name', '');
    const user_role = useLocalStorage('user_role', '');
    
    return { id, student_number, full_name, user_role };
});
