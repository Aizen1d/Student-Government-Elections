<template>
    <title>Announcements - COMELEC Portal</title>
    <Navbar></Navbar>
        
    <main class="main-margin">
        <h1 class="header">ANNOUNCEMENTS > <span class="current-page">{{ type.toUpperCase() }}</span></h1>

        <div class="category-list">
            <div class="category-list-wrapper">
                <Link href="/announcements?type=all"
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=all' || $inertia.page.url === '/announcements' }">ALL</Link>
                <Link href="/announcements?type=elections" 
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=elections' }">ELECTIONS</Link>
                <Link href="/announcements?type=debates" 
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=debates' }">DEBATES</Link>
                <Link href="/announcements?type=open_forums" 
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=open_forums' }">OPEN FORUMS</Link>
                <Link href="/announcements?type=educational_programs" 
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=educational_programs' }">EDUCATIONAL PROGRAMS</Link>
                <Link href="/announcements?type=results" 
                    class="select category" :class="{ 'active': $inertia.page.url === '/announcements?type=results' }">RESULTS</Link>
            </div>
        </div>

        <hr class="line">

        <AnnouncementsSkeleton v-if="hasFetchedAnnouncements" :loading="isAnnouncementLoading" :itemCount="3">
            <div class="announcements">
                <div class="announcements-wrapper">
                    <div class="select-announcement" v-for="(announcement, index) in announcementData" :key="index">
                        <div class="announcement-information">
                            <img :src="announcement.images[0].url" @click.prevent="onAnnouncementClick(announcement)" v-if="announcement.images.length > 0" class="announcement-img">
                            <img v-else src="" alt="?" class="announcement-img">

                            <span class="announcement-title">{{ announcement.title }}</span>
                            <span class="announcement-date">"{{ announcement.announcement_type.toUpperCase() }}"</span>
                            <span class="announcement-date">{{ toDate(announcement.created_at) }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </AnnouncementsSkeleton>

    </main>

    <Appeal></Appeal>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import AnnouncementsSkeleton from '../Skeletons/AnnouncementsSkeleton.vue'
    import Appeal from '../Shared/Appeal.vue'

    import axios from 'axios'
    import { router } from '@inertiajs/vue3'
    import { Link } from '@inertiajs/vue3'
    import { ref } from 'vue'
    import { useAnnouncementStore } from '../Stores/AnnouncementStore'
    import { useQuery } from "@tanstack/vue-query";
    import { useLocalStorage } from '@vueuse/core';

    export default{
        setup(props) {
            const type = props.type;
            const announcements = ref([]);
            const store = useAnnouncementStore();

            const hasFetchedAnnouncements = useLocalStorage('hasFetchedAnnouncements', false)

            const fetchAnnouncementType = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/${type}`, {
                    params: {
                        include_images: true
                    }
                });
                console.log(`Get all announcements (${type}) successful. Duration: ${response.duration}ms`)

                if (response.data.announcements.length === 0) {
                    hasFetchedAnnouncements.value = false;
                }
                else {
                    hasFetchedAnnouncements.value = true;
                }

                const announcements = await Promise.all(
                    response.data.announcements.map(async (announcement) => {
                        let images = announcement.images;
                        if (images.length > 0) {
                            await new Promise((resolve, reject) => {
                                let img = new Image();
                                img.src = images[0].url;
                                img.onload = resolve;
                                img.onerror = () => {
                                    images[0].url = '?'; // Set the URL to image placeholder for nonexistent images
                                    resolve();
                                };
                            });
                        }
                        return {
                            id: announcement.AnnouncementId,
                            title: announcement.AnnouncementTitle,
                            body: announcement.AnnouncementBody,
                            announcement_type: announcement.AnnouncementType,
                            attachment_type: announcement.AttachmentType,
                            created_at: announcement.created_at,
                            images,
                        };
                    })
                );

                return announcements;
            }

            const { data: announcementData,
                    isLoading: isAnnouncementLoading,
                    isSuccess: isAnnouncementSuccess,
                    isError: isAnnouncementError, } =
                    useQuery({
                        queryKey: [`announcement-${type}`],
                        queryFn: fetchAnnouncementType,
                    })

            return {
                type,
                announcements,
                store,
                hasFetchedAnnouncements,

                announcementData,
                isAnnouncementLoading,
                isAnnouncementSuccess,
                isAnnouncementError,
            }
        },
        components:{
            Standards,
            Navbar,
            Link,
            AnnouncementsSkeleton,
            Appeal,
        },
        props:{
            type: String,
        },
        methods:{
            onAnnouncementClick(item) {
                router.visit(`/announcements/view`, { 
                    data: { 
                            id: item.id 
                        }
                });
            },
            toDate(date) {
                console.log(date)
                return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
            },
        }
    }
</script>

<style scoped>
    .main-margin{
        margin: 0% 8%;
    }

    .current-page{
        color: #800000;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
    }

    .category-list{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
    }

    .category-list-wrapper{
        padding: 1.5%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0% 1%;
    }

    .select{
        text-decoration: none;
        color: black;
    }

    .select:hover,
    .select:active{
        color: #800000;
        font-weight: bold;
    }

    .active{
        color: #800000;
        font-weight: bold;
    }

    .category{
        font-size: 18px;
        margin: 0%;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .announcements{
        margin-top: 0.5%;
        margin-bottom: 1.5%;
    }

    .announcements-wrapper{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .select-announcement{
        text-decoration: none;
        color: black;
        margin: 0% 1.5%;
        margin-bottom: 2%;
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
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        transition: transform 0.4s ease;
        width: 500px;
    }

    .announcement-information:hover{
        cursor: pointer;
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