<template>
    <title>Rankings - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnElections">ONGOING ELECTIONS</span> 
            <span class="arrow"> > </span>
            <span class="header" @click.prevent="returnCurrentElection" v-if="!isElectionsLoading"> {{ electionsData.ElectionName }} </span>
            <span class="arrow"> > </span>
            Rankings
        </h1>

        <template v-if="!isElectionsLoading">
            <div class="election">
                <div class="election-wrapper">
                    <div class="election-header">
                        <div class="centered">
                            <img :src="student_org_logo" alt="" class="election-logo">
                            <span class="election-title">{{ electionsData.ElectionName  }}</span>
                            <div class="end">
                                <button class="header-button" @click="seeWinners"><img src="../../images/Rankings/result.svg" alt="" class="header-svg result"></button>
                            </div>
                        </div>
                    </div>

                    <hr class="line">

                    <div class="card-set">
                        <div class="card">
                            <div class="card-wrapper">
                                <div class="card-information">
                                    <img src="../../images/Rankings/voters.svg" alt="" class="card-svg">
                                    <div class="count">
                                        <span class="quantity">{{ totalEligibleVoters }}</span>
                                        <span class="quantity-label">Eligible Voters</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card">
                            <div class="card-wrapper">
                                <div class="card-information">
                                    <img src="../../images/Rankings/vote.svg" alt="" class="card-svg vote-svg">
                                    <div class="count">
                                        <span class="quantity">{{ totalPositionVotes }}</span>
                                        <span class="quantity-label">Votes</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card">
                            <div class="card-wrapper">
                                <div class="card-information">
                                    <img src="../../images/Rankings/abstain.svg" alt="" class="card-svg abstain-svg">
                                    <div class="count">
                                        <span class="quantity">{{ totalPositionAbstain }}</span>
                                        <span class="quantity-label">Abstained</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="dropdown">
                        <select class="filter" aria-label="Default select example" v-model="selectedPosition">
                            <option value="" disabled hidden selected>Select Position</option>
                            <option v-for="(position, index) in positionsData"
                                    :key="index" 
                                    :value="position.PositionName">
                                    {{ position.PositionName }}
                            </option>
                        </select>
                    </div>

                    <template v-if="!isRankingsLoading">
                        <div class="top-ranks">
                            <div class="top" v-if="rankOne">
                                <div class="top-wrapper">
                                    <div class="top-information">
                                        <div class="upload">
                                            <img :src="rankOne.display_photo" alt="" class="top-img">
                                            <div class="round1">
                                                <img src="../../images/Rankings/1st.svg" alt="" class="rank-svg">
                                            </div>
                                        </div>
                                        <span class="top-name">{{ rankOne.full_name }}</span>
                                        <span class="top-affiliation">{{ rankOne.partylist_name }}</span>
                                    </div>
                                </div>
                                <div class="stats row">
                                    <div class="stats-count col-4">
                                        <span class="count-quantity">{{ rankOne.votes }}</span>
                                        <img src="../../images/Rankings/vote.svg" alt="" class="count-svg vote-svg">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankOne.times_abstained }}</span>
                                        <img src="../../images/Rankings/abstain.svg" alt="" class="count-svg abstain-svg abstain">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankOne.percentage.toFixed(2) }}</span>
                                        <img src="../../images/Rankings/percent.svg" alt="" class="count-svg percent">
                                    </div>
                                </div>
                            </div>
                            
                            <div class="top" v-if="rankTwo">
                                <div class="top-wrapper">
                                    <div class="top-information">
                                        <div class="upload">
                                            <img :src="rankTwo.display_photo" alt="" class="top-img">
                                            <div class="round1">
                                                <img src="../../images/Rankings/2nd.svg" alt="" class="rank-svg">
                                            </div>
                                        </div>
                                        <span class="top-name">{{ rankTwo.full_name }}</span>
                                        <span class="top-affiliation">{{ rankTwo.partylist_name }}</span>
                                    </div>
                                </div>
                                <div class="stats row">
                                    <div class="stats-count col-4">
                                        <span class="count-quantity">{{ rankTwo.votes }}</span>
                                        <img src="../../images/Rankings/vote.svg" alt="" class="count-svg vote-svg">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankTwo.times_abstained }}</span>
                                        <img src="../../images/Rankings/abstain.svg" alt="" class="count-svg abstain-svg abstain">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankTwo.percentage.toFixed(2) }}</span>
                                        <img src="../../images/Rankings/percent.svg" alt="" class="count-svg percent">
                                    </div>
                                </div>
                            </div>

                            <div class="top" v-if="rankThree">
                                <div class="top-wrapper">
                                    <div class="top-information">
                                        <div class="upload">
                                            <img :src="rankThree.display_photo"  alt="" class="top-img">
                                            <div class="round1">
                                                <img src="../../images/Rankings/3rd.svg" alt="" class="rank-svg">
                                            </div>
                                        </div>
                                        <span class="top-name">{{ rankThree.full_name }}</span>
                                        <span class="top-affiliation">{{ rankThree.partylist_name }}</span>
                                    </div>
                                </div>
                                <div class="stats row">
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankThree.votes }}</span>
                                        <img src="../../images/Rankings/vote.svg" alt="" class="count-svg vote-svg">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankThree.times_abstained }}</span>
                                        <img src="../../images/Rankings/abstain.svg" alt="" class="count-svg abstain-svg abstain">
                                    </div>
                                    <div class="stats-count col-4">                                
                                        <span class="count-quantity">{{ rankThree.percentage.toFixed(2) }}</span>
                                        <img src="../../images/Rankings/percent.svg" alt="" class="count-svg percent">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="low-ranks">
                            <div class="low" v-for="(candidate, index) in rankingsData.results" :key="index">
                                <div class="low-wrapper" v-if="candidate.rank > 3">
                                    <div class="low-information">
                                        <span class="rank">{{ getOrdinalSuffix(candidate.rank) }}</span>
                                        <img src="default.png" alt="" class="low-img">
                                        <div class="candidate-information">
                                            <span class="candidate-name">{{ candidate.full_name }}</span>
                                            <span>{{ candidate.partylist_name }}</span>
                                        </div>

                                        <div class="statistics">
                                            <div class="stats-count1">                                        
                                                <span class="count-quantity">{{ candidate.votes }}</span>
                                                <img src="../../images/Rankings/vote.svg" alt="" class="count-svg vote-svg">
                                            </div>
                                            <div class="stats-count1 margin">                                        
                                                <span class="count-quantity">{{ candidate.times_abstained }}</span>
                                                <img src="../../images/Rankings/abstain.svg" alt="" class="count-svg abstain-svg abstain">
                                            </div>
                                            <div class="stats-count1">                                        
                                                <span class="count-quantity">{{ candidate.percentage.toFixed(2) }}</span>
                                                <img src="../../images/Rankings/percent.svg" alt="" class="count-svg percent">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </template>

                </div>
            </div>
        </template>

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
    import { useLocalStorage } from '@vueuse/core';
    import axios from 'axios';

    export default {
        setup(props) {
            const electionId = ref(Number(props.election_id));
            const selectedPosition = useLocalStorage(`selectedPosition-${electionId.value}`, '');

            const student_org_logo = ref(null);
            const totalEligibleVoters = ref(0);
            const totalPositionVotes = ref(0);
            const totalPositionAbstain = ref(0);

            const rankOne = ref(null);
            const rankTwo = ref(null);
            const rankThree = ref(null);

            const getElectionData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${electionId.value}`);
                console.log(`Get election with id ${electionId.value} successful. Duration: ${response.duration}ms`)

                return response.data.election;
            }

            const { data: electionsData,
                isLoading: isElectionsLoading,
                isSuccess: isElectionsSuccess,
                isError: isElectionsError } =
                useQuery({
                    queryKey: [`getElectionData-${electionId.value}`],
                    queryFn: getElectionData,
                })

            const getPositionsFromElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${electionId.value}`);
                console.log(`Get election with id ${electionId.value} successful. Duration: ${response.duration}ms`)

                return response.data.positions;
            }

            const { data: positionsData,
                isLoading: isPositionsLoading,
                isSuccess: isPositionsSuccess,
                isError: isPositionsError } =
                useQuery({
                    queryKey: [`getPositionsData-${electionId.value}`],
                    queryFn: getPositionsFromElection,
                })
            
            watch(selectedPosition, (newVal, oldVal) => {
                if (newVal !== '') {
                    resultsRefetch();
                }
            })

            const getPositionRankings = async () => {
                if (selectedPosition.value === '') {
                    return [];
                }

                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/votings/election/${electionId.value}/${selectedPosition.value}/results`);
                console.log(`Get ${selectedPosition.value} rankings of election ${electionId.value} successful. Duration: ${response.duration}ms`)

                student_org_logo.value = response.data.student_organization_logo;

                totalEligibleVoters.value = response.data.total_eligible_voters;
                totalPositionVotes.value = response.data.total_votes_position;
                totalPositionAbstain.value = response.data.total_abstain_count;

                // Check if response.data[0] 1 and 2 are not null
                if (response.data.results[0] !== null) {
                    rankOne.value = response.data.results[0];
                }
                else {
                    rankOne.value = null;
                }

                if (response.data.results[1] !== null) {
                    rankTwo.value = response.data.results[1];
                }
                else {
                    rankTwo.value = null;
                }

                if (response.data.results[2] !== null) {
                    rankThree.value = response.data.results[2];
                }
                else {
                    rankThree.value = null;
                }

                return response.data;
            }

            const { data: rankingsData,
                isLoading: isRankingsLoading,
                isSuccess: isRankingsSuccess,
                isError: isRankingsError,
                refetch: resultsRefetch } =
                useQuery({
                    queryKey: [`rankingsData-${electionId.value}-${selectedPosition.value}`],
                    queryFn: getPositionRankings,
                })

            // Set the selectedPosition as first of positionsData
            watch(isPositionsSuccess, (newVal, oldVal) => {
                if (newVal) {
                    selectedPosition.value = positionsData.value[0].PositionName
                }
            })

            return {
                electionId,
                selectedPosition,

                student_org_logo,
                totalEligibleVoters,
                totalPositionVotes,
                totalPositionAbstain,

                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,

                positionsData,
                isPositionsLoading,
                isPositionsSuccess,
                isPositionsError,

                rankingsData,
                isRankingsLoading,
                isRankingsSuccess,
                isRankingsError,
                resultsRefetch,

                rankOne,
                rankTwo,
                rankThree,
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
            seeWinners(){
                if (!this.isVotingPeriodEnded()) {
                    return alert('Winners page for this election is currently closed.')
                }

                router.visit('/elections/view/winners', {
                    data: {
                        id: this.electionId,
                    }
                })
            },
            isVotingPeriodEnded() {
                // Check if current datetime is above voting period
                const now = new Date();
                const end = new Date(this.rankingsData.voting_end);

                return now > end;
            },
            getOrdinalSuffix(i) {
                const j = i % 10;
                const k = i % 100;
                if (j == 1 && k != 11) {
                    return i + "st";
                }
                if (j == 2 && k != 12) {
                    return i + "nd";
                }
                if (j == 3 && k != 13) {
                    return i + "rd";
                }
                return i + "th";
            }
        },
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
        width: 70px;
        height: 70px;
        object-fit: contain;
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

    .card-set{
        display: flex;
        align-items: center;
        justify-content: space-between;
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

    .dropdown{
        margin: 1.5% 0%;
    }

    .position{
        font-size: 25px;
        font-weight: bold;
    }

    .top-ranks {
        display: flex;
        justify-content: flex-start;
    }

    .top:not(:last-child) {
        margin-right: 30px;
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
    }

    .top-wrapper{
        padding: 3%;
        display: flex; /* Add this */
        flex-direction: column; /* Add this */
        justify-content: center; /* Add this */
        align-items: center; /* Add this */
        margin-top: 57px;
    }

    .top-information{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .top-img{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
    }

    .upload{
        width: 135px;
        position: relative;
        padding: 0%;
        text-align: center;
    }
    
    .upload .round1{
        position: absolute;
        bottom: 0;
        right: 0;
        width: 38px;
        height: 38px;
        line-height: 33px;
        text-align: center;
        border-radius: 50%;
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

    .low-ranks{
        margin: 1.5% 0%;
    }

    .low{
        background-color: white;
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        margin: 2% 0%;
    }

    .low-wrapper{
        padding: 1%;
    }

    .low-information{
        display: flex;
        align-items: center;
    }

    .low-img{
        width: 85px;
        margin: 0% 1%;
    }

    .rank{
        font-size: 22px;
        font-weight: bold;
        color: #AFABAB;
        margin: 0% 1%;
    }

    .candidate-information{
        display: flex;
        flex-direction: column;
        margin: 0% 1%;
    }

    .candidate-name{
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }

    .statistics{
        display: flex;
        margin-left: auto;
        margin-right: 55px;
        align-items: center;
        justify-content: center;
    }

    .stats-count1{
        padding: 1.5%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .margin{
        margin: 0px 90px;
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

    .filter{
        width: 20%;
        height: 40px;
        padding-left: .5%;
        border-radius: 5px;
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

</style>