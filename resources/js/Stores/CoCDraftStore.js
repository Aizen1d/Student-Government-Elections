import { defineStore } from "pinia";
import { ref } from "vue";
import { useLocalStorage } from '@vueuse/core';

export const useCoCDraftStore = defineStore('cocdrafts', () => {
    let student_number = useLocalStorage('student_number', '');
    let verification_code = useLocalStorage('verication_code', '');
    let address = useLocalStorage('address', '');
    let political_affiliation = useLocalStorage('political_affiliation', '');
    let party_list = useLocalStorage('party_list', '');
    let selected_position = useLocalStorage('selected_position', '');

    let display_photo = useLocalStorage('display_photo', '');
    let display_photo_file_name = useLocalStorage('display_photo_file_name', '');

    let certification_of_grades = useLocalStorage('certification_of_grades', '');
    let certification_of_grades_file_name = useLocalStorage('certification_of_grades_file_name', '');

    return { 
        student_number,
        verification_code,
        address,
        political_affiliation,
        party_list,
        selected_position,
        display_photo,
        display_photo_file_name,
        certification_of_grades,
        certification_of_grades_file_name
    };
});
