import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
    const id = useLocalStorage('id', '');
    const student_number = useLocalStorage('student_number', '');

    const full_name = useLocalStorage('full_name', '');
    const user_role = useLocalStorage('user_role', '');

    const organization_name = useLocalStorage('organization_name', '');
    const organization_position_id = useLocalStorage('organization_position_id', '');

    const reset = () => {
        id.value = '';
        student_number.value = '';
        full_name.value = '';
        user_role.value = '';
        organization_name.value = '';
        organization_position_id.value = '';
    };
    
    return { id, student_number, full_name, user_role, organization_name, organization_position_id, reset };
});
