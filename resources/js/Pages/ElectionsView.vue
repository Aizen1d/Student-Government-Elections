<template>
    <title>Elections View - COMELEC Portal</title>
    <Navbar></Navbar>
    <div v-if="isElectionLoading"></div>
    <div v-else class="main">
        <h3 class="return" @click="returnPage">Return to list</h3>

        <div class="row">
            <div class="col-6 info">
                <h1>{{ electionData.election.ElectionName }}</h1>
                <p class="py-1">{{ electionData.election.Semester }} of S.Y. {{ electionData.election.SchoolYear }}</p>
                <p>{{ electionData.election.ElectionType }}</p>
            </div>
            <div class="col-6" style="text-align: end;">
                <ActionButton class="mx-2 px-5" @click="seeResults" :disabled="false">See Results</ActionButton>
                <ActionButton class="mx-2 px-5" @click="fileCoc" :disabled="!isFilingPeriod">File COC</ActionButton>
                <ActionButton class="mx-2 px-5" @click="registerParty" :disabled="!isFilingPeriod">Register Party</ActionButton>
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
                    Position
                </h1>
                <h1 v-else>
                    Positions
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
                const start = new Date(this.formattedElectionData.CoCFilingStart);
                const end = new Date(this.formattedElectionData.CoCFilingEnd);

                return now >= start && now <= end;
            },
        },
        methods:{
            returnPage(){
                router.visit('/elections')
            },
            seeResults(){
                router.visit('/election/view/results')
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
        },
    }
</script>

<style scoped>
    .return{
        width: fit-content;
        font-size: 20px;
        letter-spacing: 1px;
        font-weight: 800;
        margin-top: -1%;
        margin-bottom: 1.5%;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
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

    .info h1{
        font-weight: 800;
        font-size: 30px;
        color: #B90321;
    }

    .info p{
        font-size: 17px;
        margin: .5% 0%;
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
        font-size: 17px;
        line-height: 110%;
    }
</style>