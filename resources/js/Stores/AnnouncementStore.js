import { defineStore } from "pinia";
import { ref } from "vue";

export const useAnnouncementStore = defineStore('announcements', () => {
    const all = ref([]);
    const elections = ref([]);
    const debates = ref([]);
    const open_forums = ref([]);
    const educational_programs = ref([]);
    const results = ref([]);

    return { 
            all,
            elections,
            debates,
            open_forums,
            educational_programs,
            results,
        };
});
