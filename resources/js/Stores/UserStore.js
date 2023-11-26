import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
    const student_number = useLocalStorage('student_number', '');
    const full_name = useLocalStorage('full_name', '');

    const reset = () => {
        student_number.value = '';
        full_name.value = '';
    };
    
    return { student_number, full_name, reset };
});
