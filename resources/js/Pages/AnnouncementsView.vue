<template>
    <Navbar></Navbar>
    <div>
        <div class="main">
            <h3 class="return" @click="returnPage">Return to lists</h3>
            
            <Carousel :images="images" :interval="5000"></Carousel>
        </div>
        <div class="info">
            <p class="type">{{ announcement_type.toUpperCase() }}</p>
            <h1>{{ title }}</h1>
            <p>{{ body }}</p>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import Carousel from '../Shared/Carousel.vue'

    import { ref } from 'vue'
    import { useAnnouncementStore } from '../Stores/AnnouncementStore'
    import axios from 'axios'
    import { router } from '@inertiajs/vue3'

    export default{
        setup(props){
            const store = useAnnouncementStore();

            const announcement_id = ref(props.id);
            const announcement_type = ref('');
            const attachment_type = ref('');
            const title = ref('');
            const body = ref('');
            const images = ref([]);

            const currentIndex = ref(0);
            
            return{
                store,
                announcement_id,
                announcement_type,
                attachment_type,
                title,
                body,
                images,
                currentIndex,
            }
        },
        components:{
            Standards,
            Navbar,
            Carousel,
        },
        created() {
            this.fetchAnnouncement();
        },
        props: {
            id: '',
        },
        methods: {
            returnPage(){
                router.visit('/announcements');
            },
            prevSlide(){
                if (this.currentIndex > 0){
                    this.currentIndex--;
                }
                else {
                    this.currentIndex = this.images.length - 1;
                }
            },
            nextSlide(){
                if(this.currentIndex < this.images.length - 1){
                    this.currentIndex++;
                }
                else {
                    this.currentIndex = 0;
                }
            },
            fetchAnnouncement(){
                const id = Number(this.announcement_id);

                if (Object.keys(this.store.selectedAnnouncement).length > 0) { // Check if the store has an announcement
                    // Use the announcement in the store/cache if it exists
                    const announcement = this.store.selectedAnnouncement;

                    this.announcement_type = announcement.announcement_type;
                    this.attachment_type = announcement.attachment_type;
                    this.title = announcement.title;
                    this.body = announcement.body;
                    this.images = announcement.images;

                    return;
                }

                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/get/${id}`, {
                        params: {
                            include_images: true
                        }
                    })
                    .then(response => {
                    console.log(`Get announcement (${this.announcement_id}) successful. Duration: ${response.duration}ms`)

                    const announcement = response.data.announcement;
                    const data = {
                        id: this.announcement_id,
                        title: announcement.AnnouncementTitle,
                        body: announcement.AnnouncementBody,
                        announcement_type: announcement.AnnouncementType,
                        attachment_type: announcement.AttachmentType,
                        images: announcement.images,
                    };

                    this.store.selectAnnouncement(data);

                    this.announcement_type = data.announcement_type;
                    this.attachment_type = data.attachment_type;
                    this.title = data.title;
                    this.body = data.body;
                    this.images = data.images;
                });
            }
        },
    }
</script>

<style scoped>
    .return{
        margin-top: 2%;
        margin-bottom: -2%;
        font-size: 20px;
        letter-spacing: 3px;
        font-weight: 800;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .main, .info{
        margin: 0% 5%;  
    }

    .carousel-inner{
        margin: 4% 0%;
    }

    .carousel-item{
        height: 700px;
        background-color: rgba(208, 208, 208, 0.7);
    }

    .carousel-item img {
        width: 100%;
        height: 100%;
        object-fit: contain; /* This makes the image scale while maintaining its aspect ratio */
        object-position: center; /* This centers the image within its container */
    }

    .info{
        font-family: 'Source Sans Pro', sans-serif;
        margin-bottom: 4%;
    }

    .info p.type{
        font-size: 18px;
        margin-top: -1.5%;
    }

    .info h1{
        font-weight: 700;
        margin: 1.5% 0%;
    }

    .info p{
        font-size: 20px;
    }
</style>