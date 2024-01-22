<template>
    <title>Winners - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnElections">ONGOING ELECTIONS</span> 
            <span class="arrow"> > </span>
            <span class="header" @click.prevent="returnCurrentElection" v-if="!isElectionsLoading && isElectionsSuccess">{{ electionsData.election.ElectionName }}</span> 
            <span class="arrow"> > </span>
            Results
        </h1>

        <div class="election">
            <div class="election-wrapper">
                <div class="election-header" v-if="!isElectionsLoading">
                    <div class="centered">
                        <img :src="electionsData.organization_logo" alt="" class="election-logo">
                        <span class="election-title">{{ electionsData.election.ElectionName }}</span>
                    </div>
                </div>

                <hr class="line">

                <div class="congratulations-card">
                    <div class="congratulations-wrapper">
                        <div class="congratulations-information">
                            <img src="../../images/Winners/confetti.svg" alt="" class="congratulations-svg">
                            <h1 class="message">We extend our sincere congratulations to each of you on your election victories! Your leadership journeys have now officially begun.</h1>
                            <img src="../../images/Winners/fireworks.svg" alt="" class="congratulations-svg">
                        </div>
                    </div>
                </div>

                <div class="card-set">
                    <div class="card">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <img src="../../images/Winners/voters.svg" alt="" class="card-svg">
                                <div class="count">
                                    <span class="quantity" v-if="!isWinnersLoading">{{ this.winnersData.num_eligible_voters }}</span>
                                    <span class="quantity-label">Eligible Voters</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <img src="../../images/Winners/vote.svg" alt="" class="card-svg vote-svg">
                                <div class="count">
                                    <span class="quantity" v-if="!isWinnersLoading">{{ this.winnersData.total_votes }}</span>
                                    <span class="quantity-label">Votes</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <img src="../../images/Winners/abstain.svg" alt="" class="card-svg abstain-svg">
                                <div class="count">
                                    <span class="quantity" v-if="!isWinnersLoading">{{ this.winnersData.total_abstain }}</span>
                                    <span class="quantity-label">Abstained</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <template v-if="!isElectionsLoading && !isWinnersLoading">
                    <div v-for="(winnerData, position) in winnersData.winners" :key="position">
                        <div class="position-wrapper">
                            <div class="position">
                                <h1 class="position-label" v-if="!winnerData.is_tied">{{ position }}</h1>
                                <h1 class="position-label" v-else>
                                    {{ position }} - (Tied)
                                </h1>
                            </div>
                        </div>

                        <div v-if="winnerData.no_winner" class="top-ranks">
                            <h1 class="candidate">
                                (No winner)
                            </h1>
                        </div>

                        <div class="top-ranks mb-4" v-for="(candidate, candidateIndex) in winnerData.candidates" :key="candidateIndex">
                            <div class="top">
                                <div class="top-wrapper">
                                    <div class="top-information">
                                        <div class="upload">
                                            <img :src="candidate.display_photo" alt="" class="top-img">
                                        </div>
                                        <span class="top-name">{{ candidate.full_name }}</span>
                                        <span class="top-affiliation">{{ candidate.partylist }}</span>
                                        <span class="section">{{ candidate.course_code }} {{ candidate.year }}-{{ candidate.section }}</span>
                                    </div>
                                </div>
                                <div class="stats row">
                                    <div class="stats-count col-4">
                                        <span class="count-quantity">{{ candidate.votes }}</span>
                                        <img src="../../images/Winners/vote.svg" alt="" class="count-svg vote-svg">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ candidate.times_abstained }}</span>
                                        <img src="../../images/Winners/abstain.svg" alt="" class="count-svg abstain-svg abstain">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ candidate.percentage.toFixed(2) }}</span>
                                        <img src="../../images/Winners/percent.svg" alt="" class="count-svg percent">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr class="line">

                    </div>
                </template>
                
            </div>
        </div>
    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed, watch } from 'vue';
    import axios from 'axios';

    export default {
        setup(props) {
            const electionId = ref(Number(props.election_id));

            const getElectionData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${electionId.value}`);
                console.log(`Get election with id ${electionId.value} successful. Duration: ${response.duration}ms`)

                return response.data;
            }

            const { data: electionsData,
                isLoading: isElectionsLoading,
                isSuccess: isElectionsSuccess,
                isError: isElectionsError } =
                useQuery({
                    queryKey: [`getElectionData-${electionId.value}`],
                    queryFn: getElectionData,
                })

            const getWinnersFromElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/votings/get-winners/${electionId.value}`);
                console.log(`Get winners on election with id ${electionId.value} successful. Duration: ${response.duration}ms`)

                return response.data;
            }

            const { data: winnersData,
                isLoading: isWinnersLoading,
                isSuccess: isWinnersSuccess,
                isError: isWinnersError } =
                useQuery({
                    queryKey: [`getWinnersData-${electionId.value}`],
                    queryFn: getWinnersFromElection,
                })

            return {
                electionId,

                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,

                winnersData,
                isWinnersLoading,
                isWinnersSuccess,
                isWinnersError,
            }
        },
        components: {
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
            ImageSkeleton
        },
        props: {
            election_id: 0,
        },
        methods: {
            returnElections(){
                router.visit(`/elections`)
            },
            returnCurrentElection(){
                router.visit(`/elections/view?id=${this.electionId}`)
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

    .centered{
        display: flex;
        align-items: center;
    }

    .end{
        margin-left: auto;
    }

    .election{
        margin: 1.5% 0%;
    }

    .election-wrapper{
        padding: 2%;
    }

    .election-header{
        align-items: center;
    }

    .election-logo{
        width: 50px;
    }

    .election-title{
        font-size: 30px;
        font-weight: bold;
        color: #800000;
        margin: 0% 1.5%;
    }

    .election-label{
        margin: 0% 1%;
    }

    .header-svg{
        width: 35px;
    }

    .result{
        filter: invert(74%) sepia(72%) saturate(2485%) hue-rotate(349deg) brightness(104%) contrast(88%);
    }

    .header-button{
        border: transparent;
        background-color: transparent;
        align-items: center;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .congratulations-card{
        border-radius: 0%;
        border: transparent;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .congratulations-wrapper{
        padding: 1.5%;
    }

    .congratulations-information{
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .congratulations-svg{
        width: 100px;
        margin: 0px 20px;
        filter: brightness(0) saturate(100%) invert(62%) sepia(90%) saturate(630%) hue-rotate(1deg) brightness(105%) contrast(103%);
    }

    .message{
        margin: 0%;
        text-align: center;
        font-size: 25px;
    }

    .card-set{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 2% 0%;
    }

    .card{
        width: 32%;
        border-radius: 0%;
        border: transparent;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .card-wrapper{
        padding: 3%;
    }

    .card-information{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0% 3%;
    }

    .card-svg{
        width: 90px;
    }

    .count{
        display: flex;
        flex-direction: column;
        text-align: end;
    }

    .quantity{
        font-size: 50px;
    }

    .position-wrapper{
        display: flex;
        justify-content: center;
        text-align: center;
        margin: 2% 0%;
    }

    .position{
        width: 32%;
        background-color: #FFD966;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        text-align: center;
        border-radius: 6px;
    }

    .position-label{
        font-size: 28px;
        font-weight: bold;
        padding: 3%;
        margin: 0%;
    }

    .top-ranks{
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .top{
        width: 32%;
        height: 400px;
        text-align: center;
        background-color: white;
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        display: flex; 
        flex-direction: column; 
        justify-content: space-between; 
        align-items: center; /* Add this */
        margin: 0% 1%;
    }

    .top-wrapper{
        padding: 3%;
        display: flex; /* Add this */
        flex-direction: column; /* Add this */
        justify-content: center; /* Add this */
        align-items: center; /* Add this */
        margin-top: 40px;
    }

    .top-information{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .top-img{
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
    }

    .upload{
        margin-top: -20px;
    }

    .rank-svg{
        width: 38px;
        height: 38px;
        margin-bottom: 10px;
    }

    .top-name{
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 18px;
    }

    .top-affiliation{
        margin-bottom: 10px;
    }


    .stats{
        width: 100%; /* Add this */
        text-align: center; /* Add this */
        display: flex;
        align-items: center;
        justify-content: space-around; /* Change this */
        margin: 1% 0%;
        margin-bottom: 0%;
        background-color: white;
    }

    .stats-count{
        padding: 1.5%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #E7E6E6;
    }

    .count-svg{
        width: 35px;
        filter: invert(75%) sepia(0%) saturate(132%) hue-rotate(164deg) brightness(91%) contrast(82%);
    }

    .count-quantity{
        font-size: 22px;
        margin: 0px 10px;
        font-weight: bold;
    }

    .percent{
        width: 20px;
        margin: 7.5px;
    }

    .vote-svg{
        filter: invert(56%) sepia(65%) saturate(372%) hue-rotate(52deg) brightness(96%) contrast(89%);
    }

    .abstain-svg{
        filter: brightness(0) saturate(100%) invert(35%) sepia(30%) saturate(1936%) hue-rotate(320deg) brightness(106%) contrast(106%);
    }

    .abstain{
        width: 30px;
        margin: 2.5px;
    }
</style>