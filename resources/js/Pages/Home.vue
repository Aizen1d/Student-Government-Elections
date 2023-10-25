<template>
    <Navbar></Navbar>

    <div>
        <div class="main">
            <img src="../../images/Home/comelec2.jpg" class="main-ann" alt="">
        </div>

        <div class="ongoing-elections">
            <div class="header ongoing">
                <h1>ONGOING ELECTIONS</h1>
            </div>

            <div id="carouselExampleIndicators" class="carousel slide">
                <div class="carousel-indicators">
                    <button type="button" v-for="(image, index) in images" 
                        data-bs-target="#carouselExampleIndicators"
                        :data-bs-slide-to="index" 
                        :class="{ active: index === 0 }" 
                        :key="index"
                        :aria-label="'Slide ' + (index + 1)">
                    </button>
                </div>

                <div class="elections">
                    <div class="row election active">
                        <div class="col-3">
                            <div class="logo">
                                <img src="../../images/Home/puplogo.png" alt="" width="250px">
                            </div>
                        </div>
                        <div class="col-9 election-info">
                            <div class="">
                                <p class="type">SSC</p>
                                <h1>The Great SSC Vote-Off SY 2023!</h1>
                                <p class="">The filing and registration period for our upcoming election starts on <strong>October 14, 2023</strong>, 
                                    and ends on <strong>October 20, 2023</strong>. We look forward to an engaging and fair election. 
                                    Let’s make our voices heard! Remember, every vote counts.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>  

                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>

        <div class="ann">
            <div class="row header" style="display: flex;">
                <div class="col">
                    <h1>RECENT ANNOUNCEMENTS</h1>
                </div>
                <div class="col view">
                    <Link href="/announcements">VIEW ALL →</Link>
                </div>
            </div>

            <ImageSkeleton v-if="isRecentLoading" 
                            :loading="isRecentLoading" 
                            :itemCount="3" 
                            :borderRadius="'10px'"
                            :imageWidth="'27vw'" 
                            :imageHeight="'40vh'"
                            :containerMargin="'0% 1.7%'"
                            :itemMargin="'1em'">
            </ImageSkeleton>
            <div v-else class="announcements">
                <div class="row" v-for="(recent, index) in recentData" :key="index">
                    <div class="col-11 mx-4">
                        <div class="announcement" style="cursor: pointer;" @click.prevent="displaySelectedRecentAnnouncement(recent.id)">
                            <a style="text-decoration: none;">
                            <div class="pic">
                                <img v-if="recent.images.length > 0" :src="recent.images[0].url" alt="">
                                <img v-else src="" alt="">
                            </div>
                            <div class="infor" style="text-decoration: none;">
                                <span>{{ recent.announcement_type.toUpperCase()  }}</span>
                                <h1>{{ recent.title }}</h1>
                                <p class="inform">{{ recent.body }}</p>
                            </div>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="coc">
            <div class="coc-info">
                <div class="row g-5">
                    <div class="col-6">
                        <div class="coc-pic">
                            <img src="../../images/Home/coc.jpg" alt="" width="400px">
                        </div>
                    </div>
                    <div class="col-6 vertical">
                        <div class="info">
                            <h1>CAMPUS LEADERSHIP: COC NOW OR NEVER!</h1>

                            <p class="py-4">Ready to embark on this epic journey of leading our beloved university? 
                                Your COC is your ticket to the adventure – seize it now and let the campus transformation begin!
                            </p>

                            <button>Ready, Set, COC: Transform the Campus!</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="register">
            <div class="reg-info">
                <div class="row g-5">
                    <div class="col-6 vertical">
                        <div class="r-info">
                            <h1>REGISTER YOUR PARTY, IGNITE THE HEAT!</h1>

                            <p class="py-4">Ready to ignite the political fire? Register your dynamic party list, 
                                and let's set the school ablaze with your passionate campaign. 
                                Register now!
                            </p>

                            <button>Ignite Now: Register Your Party!</button>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="reg-pic">
                            <img src="../../images/Home/register.jpg" alt="" width="400px">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import Carousel from '../Shared/Carousel.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'
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
            ImageSkeleton
        },
        methods: {
            displaySelectedRecentAnnouncement(id) {
                this.store.resetSelectedAnnouncement();
                router.visit(`/announcements/view?id=${id}`);
            }
        }
    }

</script>

<style scoped>
    .main{
        height: 850px;
    }

    .main-ann{
        width: 100%;
        height: 70%;
    }

    .ongoing-elections{
        margin-top: -12% !important;
        margin: 0% 3%;
    }

    .election{
        background-image: url('../../images/Home/pupqc1-r.png');
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        margin: 2% 0%;
        height: 320px;
        object-fit: cover;
    }

    .logo{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .election-info{
        display: flex;
        align-items: center;
        height: 100%;
        width: 70%;
        font-family: 'Source Sans Pro', sans-serif;
        color: #F2F2F2;
    }

    .election-info p.type{
        font-size: 20px;
        letter-spacing: 3px;
    }

    .election-info h1{
        font-size: 40px;
        font-weight: 700;
        margin: 1.5% 0%;
    }

    .election-info p{
        font-size: 24px;
        margin-bottom: 0%;
    }

    .carousel-indicators{
        margin-bottom: 0%;
        margin-bottom: 0.25%;
    }

    .carousel-control-prev, .carousel-control-next{
        width: 70px;
    }

    .coc, .register{
        background-color: #F5F8F9;
        margin: 10% 0%;
    }

    .coc-info, .reg-info{
        margin: 0% 3% 0% 3%;
        padding: 5% 0%;

    }

    .coc-pic img, .reg-pic img{
        width: 100%;
        height: 50vh;
        object-fit: cover;
        border-radius: 7px;
    }

    .info{
        margin-left: 3%;
    }

    .r-info{
        margin-right: 3%;
    }

    .info h1, .r-info h1{
        font-family: 'Source Sans Pro Black', sans-serif;
        font-weight: 800;
        font-size: 50px;
        color: #880000;
    }

    .info p, .r-info p{
        font-size: 30px;
    }

    .info button, .r-info button{
        width: 100%;
        padding: 3% 0%;
        font-size: 30px;
        border: transparent;
        background-color: #880000;
        color: white;
    }

    .vertical{
        display: flex;
        align-items: center;
    }

    .ann{
        margin: 3% 2.5%;
    }

    .announcement a{
        display: flex;
        width: 550px;
        height: 362px;
    }

    .announcements{
        display: flex; 
        justify-content: flex-start;
        flex-wrap: wrap;
        margin: 0% 0.2%;
    }

    .announcement{
        width: 34.375em; /* 550px/16 */
        height: 22.625em; /* 362px/16 */
        padding: 0.625em; /* 10px/16 */
        position: relative;
        background-color: #880000;
        border-top-right-radius: 8%;
        border-bottom-left-radius: 7%;
    }

    .announcement .pic img {
        transition: transform .3s !important;
    }

    .announcement:hover .pic img {
        transform: scale(1.035) !important;
    }

    .announcement a::before {
        content: ""; /* This is necessary for the pseudo-element to show */
        position: absolute; /* This allows the pseudo-element to be positioned absolutely within the .announcement element */
        top: 0;
        bottom: 0;
        left: 1.25em; /* 20px/16, Adjust this to move the outline to the right */
        right: 0;
        z-index: 1;
    }

    .announcement img{
        width: 15vw;
        height: 40vh;
        object-fit: cover;
        border-radius: 7%;
        margin-left: 2%;
        margin-top: 2%;
    }

    .header{
        margin: 1.5% 0%;
    }

    .header h1{
        font-size: 20px;
        letter-spacing: 3px;
        font-weight: 800;
    }

    .view{
        text-align: end;
    }

    .header a{
        border: transparent;
        font-size: 15px;
        letter-spacing: 3px;
        font-weight: 500;
        background-color: transparent;
        text-decoration: none;
        color: #470a0a;
    }

    .infor{
        margin: 0% 3%;
        font-family: 'Source Sans Pro', sans-serif;
        color: #ffffff;
    }

    .infor span{
        font-size: 16px;
    }

    .infor h1{
        font-size: 20px;
        font-weight: bold;
        margin-top: 1.5%;
    }

    .infor p{
        height: 215px;
        width: auto;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>