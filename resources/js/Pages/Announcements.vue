<template>
    <Navbar></Navbar>
    <div>
        <div class="main">
            <div class="header my-5">
                <h1>ANNOUNCEMENTS</h1>
            </div>

            <div class="choices-container mb-3">
                <Link href="/announcements?type=all"
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=all' || $inertia.page.url === '/announcements' }">ALL</Link>
                <Link href="/announcements?type=elections" 
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=elections' }">ELECTIONS</Link>
                <Link href="/announcements?type=debates" 
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=debates' }">DEBATES</Link>
                <Link href="/announcements?type=open_forums" 
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=open_forums' }">OPEN FORUMS</Link>
                <Link href="/announcements?type=educational_programs" 
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=educational_programs' }">EDUCATIONAL PROGRAMS</Link>
                <Link href="/announcements?type=results" 
                    class="choice" :class="{ 'active': $inertia.page.url === '/announcements?type=results' }">RESULTS</Link>
            </div>
        </div>

        <AnnouncementsSkeleton :loading="isAnnouncementLoading" :itemCount="3">
            <div class="list">
                <div class="row" v-for="(announcement, index) in announcementData" :key="index">
                    <div class="col-11 column-list">
                        <div class="announcement">
                            <div class="pic">
                                <img @click.prevent="onAnnouncementClick(announcement)" v-if="announcement.images.length > 0" :src="announcement.images[0].url" alt="">
                                <img v-else src="" alt="">
                            </div>
                            <div class="info">
                                <p>{{ announcement.announcement_type.toUpperCase() }}</p>
                                <h1>{{ announcement.title }}</h1>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </AnnouncementsSkeleton>

    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import AnnouncementsSkeleton from '../Skeletons/AnnouncementsSkeleton.vue'

    import axios from 'axios'
    import { router } from '@inertiajs/vue3'
    import { Link } from '@inertiajs/vue3'
    import { ref } from 'vue'
    import { useAnnouncementStore } from '../Stores/AnnouncementStore'
    import { useQuery } from "@tanstack/vue-query";

    export default{
        setup(props) {
            const type = props.type;
            const announcements = ref([]);
            const store = useAnnouncementStore();

            const fetchAnnouncementType = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/${type}`, {
                    params: {
                        include_images: true
                    }
                });
                console.log(`Get all announcements (${type}) successful. Duration: ${response.duration}ms`)

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
            }
        }
    }
</script>

<style scoped>
.main, .list{
    margin: 0% 5%;
}

.header h1{
    font-size: 20px;
    letter-spacing: 3px;
    font-weight: 800;
}

.choices-container{
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 16px;
    font-weight: 700;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 1% 3%;
    background-color: #B90321;
}

.active{
    color: #eace2c !important;
}

.choice{
    color: lightgray;
    text-decoration: none;
}

.choice:hover{
    color: #eace2c;
}

.announcement{
    width: 100%;
    margin-top: 2em;
    margin-bottom: 2em;
}

.pic img{
    width: 100%;
    height: 33vh;
    object-fit: cover;
    transition: transform .25s ease-out;
    border-radius: 1%;
}

.pic img:hover{
    transform: scale(1.030);
    box-shadow: 1px 0px 2px 0 rgba(200, 200, 200, 0.78), 0 2px 20px 0 rgba(246, 246, 246, 0.78);  
    cursor: pointer;
}

.info{
    margin: 0% 2%;
}

.info p{
    font-size: 16px;
    margin-top: 2%;
}

.info h1{
    margin-top: -1.5%;
    font-size: 20px;
    font-weight: bold;
}

.list{
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
}

.column-list{
    margin-left: 5.5%;
}
</style>