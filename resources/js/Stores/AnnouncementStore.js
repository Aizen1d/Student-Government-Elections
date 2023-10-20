import { defineStore } from "pinia";
import { ref } from "vue";
import { useLocalStorage } from '@vueuse/core';

export const useAnnouncementStore = defineStore('announcements', () => {
    const all = ref([]);
    const elections = ref([]);
    const debates = ref([]);
    const open_forums = ref([]);
    const educational_programs = ref([]);
    const results = ref([]);

    const selectedAnnouncement = ref({})

    const selectAnnouncement = (announcement) => {
        selectedAnnouncement.value = announcement;
    }

    const resetSelectedAnnouncement = () => {
        selectedAnnouncement.value = {};
    }

    return { 
            all,
            elections,
            debates,
            open_forums,
            educational_programs,
            results,
            selectedAnnouncement,
            selectAnnouncement,  
            resetSelectedAnnouncement
        };
});
