<template>
    <title>Directory View Partylist - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnDirectory">Directory</span> 
            <span class="arrow"> > Partylists > </span>
            <span class="arrow" v-if="!isPartylistLoading"> {{ partylistData.ElectionName }} ></span>
            View Party List
        </h1>

        <div class="party-list mb-4" v-if="!isPartylistLoading">
            <div class="party-wrapper">
                <div class="party-information">
                    <div class="img-container" v-if="partylistData.ImageAttachment">
                        <img :src="partylistData.ImageAttachment" alt="" class="party-img">
                    </div>
                    
                    <hr class="line">

                    <span class="party-name">{{ partylistData.PartyListName }}</span>
                    <p class="information">
                        {{ partylistData.Description }}
                    </p>

                    <hr class="line">

                    <span class="information-label">MISSION</span>
                    <p class="information">
                        {{ partylistData.Mission }}
                    </p>

                    <hr class="line">

                    <span class="information-label">VISION</span>
                    <p class="information">
                        {{ partylistData.Vision }}
                    </p>

                    <hr class="line">

                    <span class="information-label">PLATFORMS</span>
                    <p class="information">
                        {{ partylistData.Platforms }}
                    </p>

                    <hr class="line">

                    <div class="video" v-if="partylistData.VideoAttachment">
                        <iframe class="attached-link" :src="getEmbedUrl(partylistData.VideoAttachment)" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        </div>

        <div class="party-list mb-4">
            <div class="party-wrapper">
                <div class="party-members">
                    <span class="member-header">Party Members</span>

                    <hr class="line">

                    <div class="member-list" v-if="partylistCandidates && partylistCandidates.length > 0">
                        <div class="member" v-for="(candidate, index) in partylistCandidates" :key="index">
                            <div class="candidate-wrapper">
                                <div class="candidate-position">
                                    <span class="position">{{ candidate.SelectedPositionName.toUpperCase() }}</span>                                
                                </div>
    
                                <hr class="divider">
    
                                <div class="candidate-information">
                                    <img :src="candidate.DisplayPhoto" alt="" class="candidate-img">
                                    <div class="candidate-description">
                                        <div class="spacing">
                                            <span class="candidate-name">{{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}</span>
                                            <span v-if="candidate.Rating && candidate.TimesRated">Ratings: {{ candidate.Rating / candidate.TimesRated }}</span>
                                            <span v-else>Ratings: 0</span>
                                            <div class="rate-candidate">
                                                <input type="radio" id="star5" name="rate" value="5" :checked="candidate.Rating / candidate.TimesRated >= 5" disabled/>
                                                <label for="star5" title="5 star">5 stars</label>

                                                <input type="radio" id="star4" name="rate" value="4" :checked="candidate.Rating / candidate.TimesRated >= 4 && candidate.Rating / candidate.TimesRated <= 4.99" disabled/>
                                                <label for="star4" title="4 star">4 stars</label>

                                                <input type="radio" id="star3" name="rate" value="3" :checked="candidate.Rating / candidate.TimesRated >= 3 && candidate.Rating / candidate.TimesRated <= 3.99" disabled/>
                                                <label for="star3" title="3 star">3 stars</label>

                                                <input type="radio" id="star2" name="rate" value="2" :checked="candidate.Rating / candidate.TimesRated >= 2 && candidate.Rating / candidate.TimesRated <= 2.99" disabled/>
                                                <label for="star2" title="2 star">2 stars</label>

                                                <input type="radio" id="star1" name="rate" value="1" :checked="candidate.Rating / candidate.TimesRated >= 1 && candidate.Rating / candidate.TimesRated <= 1.99" disabled/>
                                                <label for="star1" title="1 star">1 stars</label>
                                            </div>
                                        </div>
                                        <span class="etc">{{ candidate.Student.CourseCode }} {{ candidate.Student.Year }}-{{ candidate.Student.Section }}</span>
                                        <span class="motto">“{{ candidate.Motto }}”</span>
                                        <span class="platform-label">PLATFORM:</span>
                                        <p class="platform">
                                            {{ candidate.Platform }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else style="text-align: center;">
                        <h2 v-if="!isPartylistLoading && !isPartyCandidatesLoading" class="party-information">No candidates are currently running under this party list.</h2>
                    </div>
                    
                </div>
            </div>
        </div>
    </main>
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
    .main-margin{
        margin: 0% 8%;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
    }

    .current-page{
        color: #800000;
    }

    .party-list{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
    }

    .party-wrapper{
        padding: 1.5%;
    }

    .img-container{
        width: 100%;
        height: 570px;
    }

    .party-img{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .party-name{
        font-size: 28px;
        font-weight: 800;
        color: #800000;
    }

    .member-header{
        font-size: 25px;
        font-weight: 800;
        color: #800000;
    }

    .information{
        font-size: 18px;
        margin: 1% 0%;
        text-indent: 70px;
    }

    .information-label{
        font-size: 25px;
        font-weight: bold;
    }

    .video{
        width: 100%;
        height: 570px;
        background-color: rgba(224, 224, 224, 0.686);
    }

    .attached-link{
        width: 100%;
        height: 100%;
    }

    .candidate-position{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    .position{
        font-size: 22px;
        font-weight: bold;
    }

    .divider{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
    }

    .member-list{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .candidate-content{
        margin-left: 2%;
        width: 80%;
    }

    .candidate{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        margin-bottom: 2%;
    }

    .member{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        width: 780px;
        margin: 1%;
    }

    .candidate-wrapper{
        padding: 2%;
    }

    .candidate-information{
        display: flex;
    }

    .candidate-description{
        margin-left: 2%;
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    .candidate-img{
        width: 240px;
        height: 360px;
        object-fit: cover;
    }

    .spacing{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .candidate-name{
        font-weight: bold;
        font-size: 18px;
    }

    .etc{
        font-size: 18px;
        margin-bottom: 6px;
    }

    .motto{
        margin-top: 5px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }

    .platform-label{
        font-size: 18px;
        font-weight: bold;
        margin: 10px 0px;
    }

    .platform{
        font-size: 18px;
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

    .rate-candidate {
        height: 42px;
    }
    .rate-candidate:not(:checked) > input {
        position:absolute;
        top:-9999px;
    }
    .rate-candidate:not(:checked) > label {
        width:1em;
        overflow:hidden;
        white-space:nowrap;
        cursor:pointer;
        font-size:28px;
        color:#ccc;
    }
    .rate-candidate:not(:checked) > label:before {
        content: '★ ';
    }
    .rate-candidate > input:checked ~ label {
        color: #FFC000;    
    }
   
    .rate-candidate > input:checked + label:hover,
    .rate-candidate > input:checked + label:hover ~ label,
    .rate-candidate > input:checked ~ label:hover,
    .rate-candidate > input:checked ~ label:hover ~ label,
    .rate-candidate > label:hover ~ input:checked ~ label {
        color: #F6BB00;
    }
</style>