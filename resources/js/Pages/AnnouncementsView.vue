<template>
    <title>Announcements View - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">ANNOUNCEMENTS</span> 
            <span class="arrow"> ></span>
            View Announcement
        </h1>

        <div class="announcement">
            <div class="announcement-wrapper">
                <div class="announcement-information">
                    <div class="row">
                        <div class="col-6">
                            <ImageSkeleton v-if="isAnnouncementLoading" 
                                    :loading="isAnnouncementLoading" 
                                    :itemCount="1" 
                                    :borderRadius="'10px'"
                                    :imageWidth="'30vw'" 
                                    :imageHeight="'50vh'"
                                    :containerMargin="'3% 0%'"
                                :itemMargin="'1em'">
                            </ImageSkeleton>
                            <Carousel v-else :images="images" :interval="3500"></Carousel>
                        </div>
                        
                        <div class="col-6">
                            <div class="announcement-details">
                                <span class="announcement-title">{{ title }}</span>
                                <ToolTip class="mx-3">
                                    <slot>Announcement's carousel can select to next/prev or use left/right arrow keys</slot>
                                </ToolTip>
                                <div style="display: flex; justify-content: space-between;">
                                    <span class="announcement-type">{{ announcement_type.toUpperCase() }}</span>
                                    <span class="announcement-date">{{ toDate(created_at) }}</span>
                                </div>
                                <p class="announcement-content">
                                    {{ body }}
                                </p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </main>

    <Appeal></Appeal>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import Carousel from '../Shared/Carousel.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'
    import ToolTip from '../Shared/ToolTip.vue'
    import Appeal from '../Shared/Appeal.vue'

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
            const created_at = ref('');
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
                    created_at.value = announcementData.value.created_at;
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
                created_at,
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
            ToolTip,
            Appeal,
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
            toDate(date) {
                return new Date(date).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
            },
        },
    }
</script>

<style scoped>
    .main-margin{
        margin: 0% 8%;
    }

    .current-page{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: #800000 !important;
    }

    .arrow{
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .announcement{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
    }

    .announcement-wrapper{
        padding: 2%;
    }

    .announcement-information{
        display: flex;
        width: 100%;
    }

    .announcement-details{
        width: 100%;
        margin-left: 2%;
    }

    .announcement-title{
        font-size: 25px;
        font-weight: bold;
    }

    .announcement-type{
        font-size: 18px;
    }

    .announcement-date{
        font-size: 18px;
    }

    .announcement-content{
        font-size: 18px;
        text-indent: 70px;
        margin-top: 20px;
        text-align: justify;
    }
</style>