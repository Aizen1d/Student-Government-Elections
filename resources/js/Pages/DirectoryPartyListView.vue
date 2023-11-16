<template>
    <title>Directory View Partylist - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <div class="main">
        <img :src="partylistData.ImageAttachment" alt="" class="party-image" draggable="false">
    </div>

    <div class="party">
        <h1 class="eligible">
            <span class="return" @click="returnDirectory">Directory</span>&nbsp;>&nbsp;<span class="return" @click="returnSelection">Partylist Selection</span>&nbsp;>&nbsp;View
        </h1>

        <h1 class="party-name">{{ partylistData.PartyListName }}</h1>

        <p class="party-information">
            {{ partylistData.Description }}
        </p>

        <hr class="my-4">

        <h2 class="party-information-label">MISSION</h2>

        <p class="party-information">
            {{ partylistData.Mission }}
        </p>

        <hr class="my-4">

        <h2 class="party-information-label">VISION</h2>

        <p class="party-information">
            {{ partylistData.Vision }}
        </p>

        <hr class="my-4">

        <h2 class="party-information-label">PLATFORMS</h2>

        <p class="party-information">
            {{ partylistData.Platforms }}
        </p>

        <div class="video">
            <iframe class="attached-link" :src="getEmbedUrl(partylistData.VideoAttachment)" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>

        <div class="members">
            <hr class="my-5">
            <h2 class="party-member-label">PARTY MEMBERS</h2>

            <div class="members-list">
                <div class="member-card" v-for="(candidate, index) in partylistCandidates" :key="index">
                    <h3 class="position-label">{{ candidate.SelectedPositionName.toUpperCase() }}</h3>
                    <div class="member-photo">
                        <img :src="candidate.DisplayPhoto" alt="" draggable="false">
                    </div>
                    <h4 class="member-name">{{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}</h4>
                    <h6 class="member-motto">"{{ candidate.Motto }}"</h6>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed, watchEffect, watch } from 'vue';
    import axios from 'axios';

    export default {
        setup(props) {
            const partylistId = ref(props.id);

            const fetchPartylistData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/${partylistId.value}`);
                console.log(`Get partylist data successful. Duration: ${response.duration}ms`)

                return response.data.partylist;
            }

            const { data: partylistData,
                    isLoading: isPartylistLoading,
                    isSuccess: isPartylistSuccess,
                    isError: isPartylistError } =
                useQuery({
                    queryKey: [`fetchPartylistData${partylistId.value}`],
                    queryFn: fetchPartylistData,
                })
            
            const fetchPartylistCandidates = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/${partylistId.value}/candidates/all`);
                console.log(`Get all partylist candidates successful. Duration: ${response.duration}ms`)

                return response.data.candidates;
            }

            const { data: partylistCandidates,
                    isLoading: isPartyCandidatesLoading,
                    isSuccess: isPartyCandidatesSuccess,
                    isError: isPartyCandidatesError } =
                useQuery({
                    queryKey: [`fetchPartylistCandidates${partylistId.value}`],
                    queryFn: fetchPartylistCandidates,
                })

            return {
                partylistData,
                isPartylistLoading,
                isPartylistSuccess,
                isPartylistError,

                partylistCandidates,
                isPartyCandidatesLoading,
                isPartyCandidatesSuccess,
                isPartyCandidatesError,
            }
        },
        components: {
            Standards,
            Navbar,
            ActionButton
        },
        props: {
            id: '',
        },
        methods: {
            returnDirectory() {
                router.visit('/directory')
            },
            returnSelection() {
                router.visit('/directory/partylists')
            },
            getEmbedUrl(url) {
                let videoId = url.split('v=')[1];
                
                return 'https://www.youtube.com/embed/' + videoId;
            },
        }
    }
</script>

<style scoped>
    .eligible{
        font-size: 28px;
        font-weight: 800;
        margin-top: -2.5%;
        margin-bottom: 2%;
    }

    .return{
        font-size: 28px;
        font-weight: 800;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .main{
        height: 550px;
    }

    .party-image{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .party{
        margin: 3% 13%;
        text-align: justify;
    }

    .party-name{
        color: #9A000A;
        font-size: 38px;
        font-weight: 900;
    }

    .party-information{
        font-size: 20px;
        text-indent: 70px;
        margin: 1% 0%;
    }

    .party-information-label{
        color: #9A000A;
        font-size: 30px;
        font-weight: 900;
    }

    .video{
        width: 100%;
        height: 600px;
        background-color: gray;
        margin: 2% 0%;
    }

    .attached-link{
        width: 100%;
        height: 100%;
    }

    .members{
        margin: 4% 0%;
    }

    .party-member-label{
        color: #9A000A;
        font-size: 34px;
        font-weight: 900;
    }

    .members-list{
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center;
    }

    .position-label{
        color: rgb(35, 35, 34);
        font-size: 30px;
        font-weight: 900;
        margin: 2% 0%;
    }

    .member-name{
        color: rgb(35, 35, 34);
        font-size: 22px;
        font-weight: 900;
        margin: 2% 0%;
    }

    .member-motto{
        color: rgb(35, 35, 34);
        font-size: 17px;
        margin: 3% 0%;
        font-style: italic;
    }

    .member-card{
        text-align: center;
        width: 33.33%;
        margin: 1% 0%;
        transition: transform 0.3s ease;
    }

    .member-card:hover{
        transform: scale(1.02);

        .member-motto{
            color: #9A000A;
        }
    }

    .member-photo img{
        width: 250px;
        height: 250px;
        object-fit: cover;
        border-radius: 100%;
        margin: 3% 0%;
    }

    .row{
        margin: 3% 0%;
    }
</style>