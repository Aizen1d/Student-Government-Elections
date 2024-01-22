<template>
    <title>Home - COMELEC Portal</title>
    <Navbar></Navbar>

    <main>
        <div class="banner">
            <img src="../../images/Home/banner.jpg" alt="" class="banner-img">
        </div>

        <div class="features">
            <div class="features-wrapper">
                <a href="/elections" class="select-feature">
                    <div class="feature-information">
                        <img src="../../images/Home/student.png" alt="" class="feature-img">
                        <span class="feature-title">FILE FOR CANDIDACY</span>
                        <span class="feature-description">Step up, be the leader your school deserves.</span>
                    </div>
                </a>
                
                <a href="/elections" class="select-feature">
                    <div class="feature-information">
                        <img src="../../images/Home/team.png" alt="" class="feature-img">
                        <span class="feature-title">REGISTER YOUR PARTY</span>
                        <span class="feature-description">Create your crew, let your collective voices echo.</span>
                    </div>
                </a>
    
                <div class="select-feature">
                    <div class="feature-information">
                        <img src="../../images/Home/talk.png" alt="" class="feature-img">
                        <span class="feature-title">FILE AN APPEAL</span>
                        <span class="feature-description">Stand tall, question the status quo for what’s right.</span>
                    </div>
                </div>
            </div>
        </div>

        <hr class="line">
        
        <div class="header">
            <div>
                <span class="header-title">RECENT ANNOUNCEMENTS</span>
            </div>
            <div>
                <button class="view-button" @click.prevent="redirectToAllAnnouncements">View All</button>
            </div>
        </div>
        
        <ImageSkeleton v-if="isRecentLoading" 
                            :loading="isRecentLoading" 
                            :itemCount="2" 
                            :borderRadius="'10px'"
                            :imageWidth="'27vw'" 
                            :imageHeight="'40vh'"
                            :containerMargin="'0% 1.7%'"
                            :itemMargin="'1em'">
        </ImageSkeleton>
        <div v-else class="announcements">
            <div class="announcements-wrapper">
                <div v-for="(recent, index) in recentData" :key="index" class="select-announcement" style="cursor: pointer;" @click.prevent="displaySelectedRecentAnnouncement(recent.id)">
                    <div class="announcement-information">
                        <img class="announcement-img" v-if="recent.images.length > 0" :src="recent.images[0].url" alt="">
                        <img class="announcement-img" v-else src="" alt="?">
                        <span class="announcement-title">{{ recent.title }}</span>
                        <span class="announcement-date">{{ formatDate(recent.created_at) }}</span>
                    </div>
                </div>
            </div>
        </div>

        <hr class="line">
    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import Carousel from '../Shared/Carousel.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'
    import Appeal from '../Shared/Appeal.vue'
    import { Link, router } from '@inertiajs/vue3'

    import { ref } from 'vue'
    import { useQuery } from "@tanstack/vue-query";
    import { useAnnouncementStore } from '../Stores/AnnouncementStore'

    import axios from 'axios'

    export default {
        setup() {
            const images = ref(['../../images/Home/puplogo.png'])
            const recent_announcements = ref([])

            const store = useAnnouncementStore()

            const fetchRecentAnnouncements = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/all`, {
                    params: {
                        include_images: true
                    }
                })

                console.log(`Get all recent announcements successful. Duration: ${response.duration}ms`)

                const announcements = response.data.announcements.map(announcement => ({
                    id: announcement.AnnouncementId,
                    title: announcement.AnnouncementTitle,
                    body: announcement.AnnouncementBody,
                    announcement_type: announcement.AnnouncementType,
                    attachment_type: announcement.AttachmentType,
                    images: announcement.images,
                    created_at: announcement.created_at,
                }))

                return announcements.slice(0, 3)
            }

            const { data: recentData, 
                    isLoading: isRecentLoading, 
                    isSuccess: isRecentSucess, 
                    isError: isRecentError, } = 
                    useQuery({
                        queryKey: ['recentAnnouncements'],
                        queryFn: fetchRecentAnnouncements,
                    })

            return {
                images,
                recent_announcements,
                store,

                recentData,
                isRecentLoading,
                isRecentSucess,
                isRecentError,
            }
        },
        components: {
            Standards,
            Navbar,
            Carousel,
            Link,
            ImageSkeleton,
            Appeal,
        },
        methods: {
            redirectToAllAnnouncements() {
                router.visit('/announcements');
            },
            displaySelectedRecentAnnouncement(id) {
                router.visit(`/announcements/view?id=${id}`);
            },
            redirectToElection() {
                router.visit('/elections');
            },
            formatDate(date) {
                return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            },
            appeal() {
                this.$modal.show(Appeal)
            }
        }
    }

</script>

<style scoped>

.banner{
    height: 600px;
}

.banner-img{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.features{
    margin: 2.5% 0%;
}

.features-wrapper{
    margin: 0% 8%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
}

.select-feature{
    text-decoration: none;
    color: black;
}

.select-feature:hover{
    color: black;
    .feature-information{
        transform: translateY(-10px);
    }
}

.feature-information{
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 300px;
    height: 300px;
    border-radius: 5px;
    box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    transition: transform 0.4s ease;
}

.feature-img{
    height: 150px;
}

.feature-title{
    font-weight: bold;
    font-size: 22px;
    margin-top: 20px;
}

.feature-description{
    text-align: center;
    font-size: 18px;
    margin: 0px 30px;
}

.line{
    border: 0;
    height: 2px;
    background: rgb(249,249,249);
    background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
}

.header{
    margin-top: 2.5% !important;
    margin: 0% 8%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title{
    font-size: 28px;
    font-weight: bold;
}

.view-button{
    border: transparent;
    background-color: transparent;
    font-size: 20px;
}

.view-button:hover{
    color: #800000;
}

.announcements{
    margin-top: 0.5%;
    margin-bottom: 1.5%;
}

.announcements-wrapper{
    margin: 0% 8%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.select-announcement{
    text-decoration: none;
    color: black;
    margin: 1% 0.98%;
}

.select-announcement:hover{
    color: black;
    .announcement-information{
        transform: scale(1.009);
    }
}

.announcement-information{
    display: flex;
    justify-content: center;
    align-items: start;
    flex-direction: column;
    box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    transition: transform 0.4s ease;
    width: 500px;
}

.announcement-img{
    width: 500px;
    height: 273px;
    object-fit: cover;
}

.announcement-title{
    font-weight: bold;
    font-size: 18px;
    margin: 0px 5px
}

.announcement-date{
    font-size: 18px;
    margin: 0px 5px
}
</style>