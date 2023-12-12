<template>
    <Navbar></Navbar>
    <title>Home - Voting System</title>

    <div class="main">
        <h1 class="header-label">ELECTIONS</h1>

        <template v-if="atleastOneElection && !isElectionsLoading" v-for="(election, index) in electionsData" :key="index">
            <div v-if="isVotingPeriod(election)" class="select-election" @click="electionSelected(election)">
                <div :class="{ 'election': !election.is_student_voted, 'voted-already': election.is_student_voted  }">
                    <div class="election-content">
                        <img src="" alt="?" class="organization-logo">
                        <h1 class="election-title">{{ election.name }}</h1>
                    </div>
                </div>
            </div>
            <div v-if="activeElectionQuantity === 0" style="text-align: center; margin-top: 3%;">
                <h2>
                    No voting period for election at the moment.
                </h2>
            </div>
        </template>
        <div v-if="!atleastOneElection && !isElectionsLoading">
            <h1>No voting period for election at the moment.</h1>
        </div>
    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';
    import { useUserStore } from '../Stores/UserStore.js';

    import { ref } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'
    import { useLocalStorage } from '@vueuse/core';

    export default {
        setup(props) {
            const userStore = useUserStore();
            const atleastOneElection = ref(useLocalStorage('atleastOneElection', false));
            const activeElectionQuantity = ref(0);

            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            
            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all/is-student-voted`, {
                    params: {
                        student_number: userStore.student_number,
                    }
                });
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                const elections = response.data.elections.map(election => ({
                    id: election.ElectionId,
                    name: election.ElectionName,
                    type: election.ElectionType,
                    status: election.ElectionStatus,
                    voting_start: election.VotingStart,
                    voting_end: election.VotingEnd,
                    is_student_voted: election.IsStudentVoted,
                }));

                if (response.data.elections.length > 0){
                    atleastOneElection.value = true;
                }
                else {
                    atleastOneElection.value = false;
                }

                return elections;
            }

            const { data: electionsData,
                    isLoading: isElectionsLoading,
                    isSuccess: isElectionsSuccess,
                    isError: isElectionsError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            return {
                atleastOneElection,
                activeElectionQuantity,
                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,
            };
        },
        components: { Navbar },
        props: {
            student_number: '',
            full_name: '',
        },
        methods: {
            electionSelected(election){
                if (election.is_student_voted) {
                    alert('You have already voted for this election.');
                    return;
                }

                // Incase voting period ends while the user is choosing an election
                if (!this.isVotingPeriod(election)) {
                    alert('This election is not yet open for voting.');
                    return;
                }

                router.visit('/voting/process', {
                    data: {
                        id: election.id,
                    }
                })
            },
            isVotingPeriod(election){
                const now = new Date();
                const voting_start = new Date(election.voting_start);
                const voting_end = new Date(election.voting_end);

                if (now >= voting_start && now < voting_end) {
                    this.activeElectionQuantity++;
                    return true;
                }
                else {
                    return false;
                }
            },
        }
    };
</script>

<style scoped>
    .main{
        margin: 1.5% 8%
    }

    .header-label{
        font-weight: 700;
        font-size: 30px;
        color: #800000;
        margin: 0;
    }

    .select-election{
        text-decoration: none;
        color: black;
    }

    .select-election:hover{
        cursor: pointer;
    }

    .election {
        margin: 1.5% 0%;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .election::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgb(211, 211, 211);
        transition: all 600ms ease-out;
    }

    .election:hover::before {
        left: 0;
    }

    .voted-already{
        background-color: rgb(169, 169, 169);
    }

    .voted-already:hover{
        cursor: default;
    }

    .election-content {
        padding: 1.5%;
        display: flex;
        align-items: center;
        position: relative;
    }

    .organization-logo{
        width: 70px;
        height: 70px;
    }

    .election-title{
        margin: 0% 0% 0% 3%;
        width: 100%;
        font-weight: 700;
        font-size: 30px;
    }
    
</style>