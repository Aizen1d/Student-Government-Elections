<template>
    <Navbar></Navbar>
    <title>Home - Voting System</title>

    <div class="main">
        <div style="text-align: center;">
            <h1 class="header-label">ELECTIONS</h1>
        </div>
        
        <template v-if="!isElectionsLoading">
            <template v-if="electionsData.elections.AtleastOneAvailableElection">
                <template v-for="(election, index) in electionsData.elections.data" :key="index">
                    <div v-if="isVotingPeriod(election) && election.IsStudentEligible" 
                        class="select-election" @click="electionSelected(election)">
                        <div :class="{ 'election': !election.IsStudentVoted, 'voted-already': election.IsStudentVoted  }">
                            <div class="election-content">
                                <img :src="election.OrganizationLogo" alt="" class="organization-logo">
                                <h1 class="election-title">{{ election.ElectionName }}</h1>
                            </div>
                        </div>
                    </div>
                </template>
            </template>

            <!-- Display 'No available elections' if AtleastOneAvailableElection is false -->
            <template v-else>
                <div class="no-available-elections" style="text-align: center; margin-top: 3%; font-family: 'Inter', sans-serif;">
                    <h1 style="font-size: 35px;">(No available elections for you at the moment)</h1>
                </div>
            </template>
        </template>

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
            
            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all/is-student-voted`, {
                    params: {
                        student_number: userStore.student_number,
                    }
                });
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                return response.data;
            }

            const { data: electionsData,
                    isLoading: isElectionsLoading,
                    isSuccess: isElectionsSuccess,
                    isError: isElectionsError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            const getFullName = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/fullname/${props.student_number}`)
                
                userStore.full_name = response.data.full_name
                
                return response.data;
            }

            const { data: studentData,
                    isLoading: isStudentLoading,} =
                    useQuery({
                        queryKey: ['getFullName'],
                        queryFn: getFullName,
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
        },
        methods: {
            electionSelected(election){
                if (election.IsStudentVoted) {
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
                        id: election.ElectionId,
                    }
                })
            },
            isVotingPeriod(election){
                const now = new Date();
                const voting_start = new Date(election.VotingStart);
                const voting_end = new Date(election.VotingEnd);

                if (now >= voting_start && now < voting_end) {
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
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        font-size: 38px;
        color: #800000;
        margin: 0;
        margin-bottom: 2%;
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
        font-weight: 800;
        font-size: 30px;
        font-family: 'Inter', sans-serif;
    }
    
</style>