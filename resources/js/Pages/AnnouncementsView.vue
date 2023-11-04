<template>
    <title>Announcements View - COMELEC Portal</title>
    <Navbar></Navbar>
    <div>
        <div class="main">
            <h3 class="return" @click="returnPage">Return to lists</h3>
            
            <ImageSkeleton v-if="isAnnouncementLoading" 
                            :loading="isAnnouncementLoading" 
                            :itemCount="1" 
                            :borderRadius="'10px'"
                            :imageWidth="'88vw'" 
                            :imageHeight="'70vh'"
                            :containerMargin="'3% 0%'"
                            :itemMargin="'1em'">
            </ImageSkeleton>
            <Carousel v-else :images="images" :interval="5000"></Carousel>
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
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'

    import { ref, watchEffect } from 'vue'
    import { useAnnouncementStore } from '../Stores/AnnouncementStore'
    import { router } from '@inertiajs/vue3'
    import { useQuery } from "@tanstack/vue-query";

    import axios from 'axios'

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

            const fetchAnnouncement = async () => {
                const id = Number(announcement_id.value);

                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/get/${id}`, {
                    params: {
                        include_images: true
                    }
                });
                console.log(`Get announcement (${id}) successful. Duration: ${response.duration}ms`)

                return response.data.announcement;
            }

            const { data: announcementData,
                    isLoading: isAnnouncementLoading,
                    isSuccess: isAnnouncementSuccess,
                    isError: isAnnouncementError, } =
                    useQuery({
                        queryKey: [`announcement-${announcement_id.value}`],
                        queryFn: fetchAnnouncement,
                    })

            watchEffect(() => {
                if (isAnnouncementSuccess.value) {
                    announcement_type.value = announcementData.value.AnnouncementType;
                    attachment_type.value = announcementData.value.AttachmentType;
                    title.value = announcementData.value.AnnouncementTitle;
                    body.value = announcementData.value.AnnouncementBody;
                    images.value = announcementData.value.images;
                }
            });
            
            return{
                store,
                announcement_id,
                announcement_type,
                attachment_type,
                title,
                body,
                images,
                currentIndex,

                announcementData,
                isAnnouncementLoading,
                isAnnouncementSuccess,
                isAnnouncementError,
            }
        },
        components:{
            Standards,
            Navbar,
            Carousel,
            ImageSkeleton,
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