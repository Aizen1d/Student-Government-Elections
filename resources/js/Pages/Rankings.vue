<template>
    <title>Rankings - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="main">
        <div class="col">
            <h1 class="path" v-if="!isElectionsLoading">
                <span class="return" @click="returnPage">{{ electionsData.ElectionName }}</span>&nbsp;>&nbsp;Rankings
            </h1>
        </div>

        <div class="candidates-votes">
            <div class="col-2 filterDropDown">
                <input type="hidden" name="filter-type">
                <select class="filter mx-3" aria-label="Default select example" v-model="selectedPosition">
                    <option value="" disabled hidden selected>Select Position</option>
                    <option v-for="(position, index) in positionsData"
                            :key="index" 
                            :value="position.PositionName">
                            {{ position.PositionName }}
                    </option>
                </select>
            </div>
            <div v-for="(result, index) in rankingsData" :key="index">
                <div :class="result.rank === 1 ? 'candidate1' : result.rank === 2 ? 'candidate2' : result.rank === 3 ? 'candidate3' : 'candidate'">
                    <div class="candidate-information">
                        <span class="rank">{{ getOrdinalSuffix(result.rank) }}</span>
                        <img :src="result.display_photo" alt="" class="candidate-photo">
                        <span class="candidate-name">{{ result.full_name }}</span>

                        <div class="vote-count">
                            <span>{{ result.votes }} {{ result.votes > 1 ? 'votes' : 'vote' }}</span>
                            <span>{{ result.percentage.toFixed(2) }}%</span>
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
                resultsRefetch
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
    .main{
        margin: 2% 5%;
        font-family: 'Inter', sans-serif;
    }

    .filter{
        margin-top: 10% !important;
        padding-left: 3%;
        width: 100%;
        height: 40px;
        border-radius: 8px;
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .filterDropDown{
        margin-left: 1%;
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

    .candidates-votes{
        min-height: 6rem;
        max-height: 45rem;
        padding-bottom: 0.5%;
        margin: 1.5% 0%;
        background-color: white;
        border-radius: 6px;
        overflow-y: auto;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.3);
    }

    .position{
        font-weight: 900;
        font-size: 27px;
        margin: 0%;
    }

    .dropdown{
        padding: 1.5% 2% 0% 2%;
    }

    .candidate{
        margin: 1.5% 2%;
        background-color: white;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate:hover{
        box-shadow: 0px 5px 7px rgba(167, 165, 165, 0.7);
    }

    .candidate1{
        background-color: rgb(255,235,131);
        background: linear-gradient(90deg, rgba(255,235,131,1) 0%, rgba(255,214,83,1) 50%, rgba(255,230,139,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        transition: all 0.2s ease-in-out;
    }

    .candidate1:hover{
        box-shadow: 0px 5px 7px rgba(167, 165, 165, 0.7);
    }

    .candidate2{
        background: rgb(237,237,237);
        background: linear-gradient(90deg, rgba(237,237,237,1) 0%, rgba(208,206,206,1) 50%, rgba(242,242,242,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        transition: all 0.2s ease-in-out;
    }

    .candidate2:hover{
        box-shadow: 0px 5px 7px rgba(167, 165, 165, 0.7);
    }

    .candidate3{
        background: rgb(239,194,113);
        background: linear-gradient(90deg, rgba(239,194,113,1) 0%, rgba(188,128,8,1) 50%, rgba(250,219,156,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate3:hover{
        box-shadow: 0px 5px 7px rgba(167, 165, 165, 0.7);
    }

    .candidate-information{
        display: flex;
        align-items: center;
        position: relative;
        padding: 0.5% 2%;
    }

    .rank{
        font-size: 30px;
        font-weight: 900;
        margin: 0%;
        padding: 0%;
        width: 70px;
        text-align: center;
    }

    .candidate-photo{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0% 1.5%;
    }

    .candidate-name{
        font-size: 20px;
        font-weight: bold;
    }

    .vote-count{
        display: flex;
        flex-direction: column;
        text-align: end;
        position: absolute;
        right: 2%;
        font-weight: bold;
        font-size: 18px;
    }
</style>