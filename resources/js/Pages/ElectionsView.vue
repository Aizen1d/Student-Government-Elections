<template>
    <title>Elections View - COMELEC Portal</title>
    <Navbar></Navbar>

    <div v-if="isElectionLoading"></div>
    <div v-else class="main">

        <div class="row">
            <div class="col-4">
                <h1 class="path">
                    <span class="return" @click="returnPage">Elections</span>&nbsp;>&nbsp;{{ electionData.election.ElectionName }}
                </h1>

                <div class="my-2">
                    <h1 class="py-1 election-label">{{ electionData.election.Semester }} of S.Y. {{ electionData.election.SchoolYear }}</h1>
                    <h1 class="election-label">{{ electionData.election.ElectionType }} Organization</h1>
                </div>
            </div>
            <div class="col-8" style="text-align: end;">
                <ActionButton class="mx-2 px-5 action-button" @click="seeCandidates" :disabled="false">Candidates</ActionButton>
                <ActionButton class="mx-2 px-5 action-button" @click="fileCoc" :disabled="!isFilingPeriod">File a COC</ActionButton>
                <ActionButton class="mx-2 px-5 action-button" @click="registerParty" :disabled="!isFilingPeriod">Register Party</ActionButton>
                <div class="my-3"></div>
                <ActionButton class="mx-2 px-5 action-button" @click="seePartylists" :disabled="false">Partylists</ActionButton>
                <ActionButton class="mx-2 px-5 action-button" @click="seeRankings" :disabled="!isAboveVotingStartPeriod">Rankings</ActionButton>
                <ActionButton class="mx-2 px-5 action-button" @click="seeWinners" :disabled="!isVotingPeriodEnded">Winners</ActionButton>
            </div>
        </div>

        <hr>

        <div class="timeline">
            <h1>Election Timeline</h1>
            <div class="card text-center">
                <div class="card-body">
                    <h6 class="card-title">ELECTION PERIOD</h6>
                    <p class="card-text">{{ formattedElectionData.ElectionStart }}
                        <br> to <br>{{ formattedElectionData.ElectionEnd }}
                    </p>
                </div>
            </div>
            
            <div class="row my-4">
                <div class="col-xl-3 col-sm-6d-flex">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class="card-title">FILING PERIOD</h6>
                            <p class="card-text">{{ formattedElectionData.CoCFilingStart }}
                                <br> to <br>{{ formattedElectionData.CoCFilingEnd }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-sm-6d-flex">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class="card-title">CAMPAIGN PERIOD</h6>
                            <p class="card-text">{{ formattedElectionData.CampaignStart }}
                                <br> to <br>{{ formattedElectionData.CampaignEnd }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-sm-6d-flex">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class="card-title">VOTING PERIOD</h6>
                            <p class="card-text">{{ formattedElectionData.VotingStart }}
                                <br> to <br>{{ formattedElectionData.VotingEnd }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-xl-3 col-sm-6d-flex">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class="card-title">APPEAL PERIOD</h6>
                            <p class="card-text">{{ formattedElectionData.AppealStart }}
                                <br> to <br>{{ formattedElectionData.AppealEnd }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <hr>
            
            <div class="positions">
                <h1 v-if="electionData.positions.length <= 1">
                    Position and Winner Quantity
                </h1>
                <h1 v-else>
                    Positions and Winner Quantity
                </h1>
                <ul v-for="(position, index) in electionData.positions" :key="index">
                    <li>{{ position.PositionName }} ({{ position.PositionQuantity }})</li>
                </ul>  
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'

    import axios from 'axios'
    import { ref, watch, watchEffect } from 'vue'
    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';

    export default {
        setup(props) {
            const id = ref(Number(props.id))
            let formattedElectionData = ref(null);

            const fetchElectionView = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${id.value}`)

                return response.data;
            }

            const { data: electionData,
                    isLoading: isElectionLoading,
                    isSuccess: isElectionSuccess,
                    isError: isElectionError, } =
                    useQuery({
                        queryKey: [`electionView-${id.value}`],
                        queryFn: fetchElectionView,
                    })

            const getPartylistsOnThisElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/election/${id.value}`)
                console.log(`Get partylists on election with id ${id.value} successful. Duration: ${response.duration}ms`)

                return response.data.partylists;
            }

            const { data: partylistsData,
                    isLoading: isPartylistsLoading,
                    isSuccess: isPartylistsSuccess,
                    isError: isPartylistsError, } =
                    useQuery({
                        queryKey: [`getPartylistsOnThisElection-${id.value}`],
                        queryFn: getPartylistsOnThisElection,
                    })

            const formatDate = (dateString) => {
                const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
                return dateString ? new Date(dateString).toLocaleString('en-US', options) : '';
            }

            watchEffect(() => {
                if (isElectionSuccess.value) {
                    formattedElectionData.value = {
                        ...electionData.value,
                        ElectionStart: formatDate(electionData.value.election.ElectionStart),
                        ElectionEnd: formatDate(electionData.value.election.ElectionEnd),
                        CoCFilingStart: formatDate(electionData.value.election.CoCFilingStart),
                        CoCFilingEnd: formatDate(electionData.value.election.CoCFilingEnd),
                        CampaignStart: formatDate(electionData.value.election.CampaignStart),
                        CampaignEnd: formatDate(electionData.value.election.CampaignEnd),
                        VotingStart: formatDate(electionData.value.election.VotingStart),
                        VotingEnd: formatDate(electionData.value.election.VotingEnd),
                        AppealStart: formatDate(electionData.value.election.AppealStart),
                        AppealEnd: formatDate(electionData.value.election.AppealEnd),
                    };
                }
            })

            return {
                id,

                electionData,
                isElectionLoading,
                isElectionSuccess,
                isElectionError,

                partylistsData,
                isPartylistsLoading,
                isPartylistsSuccess,
                isPartylistsError,

                formattedElectionData,
            }
        },
        components:{
            Standards,
            Navbar,
            ActionButton,
        },
        props: {
            id: '',
        },
        computed: {
            isFilingPeriod() {
                // Check if current datetime is within filing period
                const now = new Date();
                const start = new Date(this.electionData.election.CoCFilingStart);
                const end = new Date(this.electionData.election.CoCFilingEnd);

                return now >= start && now < end;
            },
            isAboveVotingStartPeriod() {
                // Check if current datetime is above voting period
                const now = new Date();
                const end = new Date(this.electionData.election.VotingStart);

                return now > end;
            },
            isVotingPeriodEnded() {
                // Check if current datetime is above voting period
                const now = new Date();
                const end = new Date(this.electionData.election.VotingEnd);

                return now > end;
            },
        },
        methods:{
            returnPage(){
                router.visit('/elections')
            },
            seeCandidates(){
                router.visit(`/directory/candidates/view`, {
                    data: {
                        id: this.id,
                    }
                })
            },  
            fileCoc(){
                router.visit('/elections/view/file-coc', {
                    data: {
                        id: this.id,
                    }
                })
            },
            registerParty(){
                router.visit('/elections/view/register-party', {
                    data: {
                        id: this.id,
                    }
                })
            },
            seePartylists(){
                if (this.partylistsData.length < 1) {
                    return alert('There are no partylists registered for this election yet.')
                }

                router.visit('/directory/partylists')
            },
            seeRankings(){
                router.visit('/elections/view/rankings', {
                    data: {
                        id: this.id,
                    }
                })
            },
            seeWinners(){
                router.visit('/elections/view/winners', {
                    data: {
                        id: this.id,
                    }
                })
            },
        },
    }
</script>

<style scoped>
    .return{
        font-weight: 800;
        font-size: 30px;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .path{
        font-weight: 800;
        font-size: 30px;
        color: black;
    }

    .election-label{
        font-weight: lighter;
        font-size: 16px;
        color: rgb(20, 20, 20);
    }
    .action-button{
        width: 13rem !important;
        height: 2.7rem !important;
    }

    .card{
        border: none;
        border-radius: 10px;
        background-color: #F5F8F9;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.1);  
    }
    .main{
        margin: 3% 5%;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .btns{
        display: flex;
        justify-content: space-between;
    }

    .btns button{
        font-size: 16px;
        width: 10.9375em;
        height: 3.15em;
        border: transparent;
        border-radius: 10px;
        background-color: #850000;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.09), 0 6px 20px 0 rgba(0, 0, 0, 0.09);  
        color: white;
        font-family: 'Source Sans Pro', sans-serif;
        transition: background-color 0.12s ease-in-out;
    }

    .btns button:hover{
        cursor: pointer;
        background-color: #9b0000    
    }

    .btns button:disabled{
        background-color: #d9d9d9;
        color: black;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.07);  
    }

    .timeline h6{
        font-weight: 900;
    }

    .timeline h1{
        margin: 1% 0%;
        font-weight: 800;
        font-size: 25px;
    }

    .positions li{
        margin-top: 1%;
        line-height: 110%;

        font-weight: lighter;
        font-size: 18px;
        color: black;
    }
</style>