<template>
    <title>Winners - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="main">
        <div class="col" style="margin-left: 5%;">
            <h1 class="path" v-if="!isElectionsLoading">
                <span class="return" @click="returnPage">{{ electionsData.ElectionName }}</span>&nbsp;>&nbsp;Winners
            </h1>
        </div>
        
        <div class="header">
            <h1 class="election-label">{{ electionsData.ElectionName }}</h1>
            <h2 class="phrase">We extend our sincere congratulations to each of you on your election victories. Your leadership journeys have now officially begun.</h2>
        </div>

        <template v-if="!isElectionsLoading && !isWinnersLoading">
            <div v-for="(winnerData, position) in winnersData" :key="position">
                <h1 class="position candidate">{{ position }}</h1>

                <h1 class="candidate" v-if="winnerData.is_tied">
                    (Tied)
                </h1>

                <div v-for="(candidate, candidateIndex) in winnerData.candidates" :key="candidateIndex" class="candidate">
                    <div class="candidate-information-wrapper">
                        <div class="candidate-information">
                            <img :src="candidate.display_photo" alt="" class="candidate-photo">
                            <h1 class="candidate-name">{{ candidate.full_name }}</h1>
                            <h2 class="candidate-affiliation">{{ candidate.partylist }}</h2>
                            <h2 class="candidate-affiliation">{{ candidate.votes }} votes</h2>
                        </div>
                    </div>
                </div>

                <!-- Display 'No winner' if there's no winner for this position -->
                <div v-if="winnerData.no_winner" class="no-winner">
                    <h1 class="candidate">
                        (No winner)
                    </h1>
                </div>
            </div>
        </template>
        <template v-else>
            <div class="skeleton">
                <h3 class="candidate">LOADING..</h3>
            </div>
        </template>
    </div>
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

            const getWinnersFromElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/votings/get-winners/${electionId.value}`);
                console.log(`Get winners on election with id ${electionId.value} successful. Duration: ${response.duration}ms`)

                return response.data.winners;
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

                positionsData,
                isPositionsLoading,
                isPositionsSuccess,
                isPositionsError,

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
            returnPage(){
                router.visit(`/elections/view?id=${this.electionId}`)
            },
        },
    }
</script>

<style scoped>
    .main{
        margin: 1.5% 0%;
        font-family: 'Inter', sans-serif;
    }

    .header{
        text-align: center;
    }

    .return{
        font-weight: 700;
        font-size: 30px;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .path{
        font-weight: 700;
        font-size: 30px;
        color: black;
    }

    .election-label{
        font-family: 'Inter Black', sans-serif;
        font-weight: 700;
        font-size: 35px;        
        color: #B90321;
        margin: 0%;
    }

    .phrase{
        font-size: 18px;
        color: black;
        margin: 1% 28%;
    }

    .candidate{
        padding: 1%;
        width: 100%;
        text-align: center;
    }

    .position{
        font-weight: 800;
        font-size: 30px;
        margin: 0%;
        text-transform: uppercase;
        color: #B90321;
        letter-spacing: 1px;
    }

    .candidate-information-wrapper{
        display: flex;
        justify-content: center;
        margin: 0%;
        width: 100%;
        flex-wrap: wrap;
    }

    .candidate-information{
        width: 300px;
        height: 300px;
        padding: 1%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 1% 1%;
    }

    .candidate-photo{
        width: 170px;
        height: 170px;
        margin-top: -10%;
        margin-bottom: 5%;
        border-radius: 50%;
        object-fit: cover;
    }

    .candidate-name{
        font-size: 20px;
        margin: 3% 0%;
        font-weight: 800;
    }

    .candidate-affiliation{
        font-size: 18px;
    }
</style>