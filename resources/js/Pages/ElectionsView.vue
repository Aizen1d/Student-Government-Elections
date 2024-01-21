<template>
    <title>Elections View - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin" v-if="isElectionSuccess">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">ONGOING ELECTIONS</span> 
            <span class="arrow"> ></span>
            {{ electionData.election.ElectionName }} 
        </h1>

        <div class="election">
            <div class="election-wrapper">
                <div class="election-header">
                    <div class="centered">
                        <img :src="electionData.organization_logo" alt="" class="election-logo">
                        <span class="election-title">{{ electionData.election.ElectionName }}</span>
                        <span class="election-label">{{ electionData.student_organization_name }}</span>
                        <span class="election-label">{{ electionData.election.Semester }} of S.Y {{ electionData.election.SchoolYear }}</span>
                        <div class="end">
                            <button class="header-button" @click.prevent="seeCandidates">
                                <img src="../../images/Elections/voters.svg" alt="" class="header-svg">
                            </button>

                            <button class="header-button mx-3" @click.prevent="seeRankings" :disabled="!isAboveVotingStartPeriod">
                                <img src="../../images/Elections/rank.svg" alt="" class="header-svg" :class="{ 'isRankingsDisabled': !isAboveVotingStartPeriod }">
                            </button>

                            <button class="header-button" @click.prevent="seeWinners" :disabled="!isVotingPeriodEnded">
                                <img src="../../images/Elections/result.svg" alt="" class="header-svg result" :class="{ 'isWinnersDisabled': !isVotingPeriodEnded }">
                            </button>
                        </div>
                    </div>
                </div>

                <hr class="line">

                <div class="card-set">
                    <div class="card" @mouseenter="toggleCardHover('candidate', 'enter')" @mouseleave="toggleCardHover('candidate', 'leave')">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <span v-if="!checkCardIfHovered('candidate')" class="quantity-label" style="color: #800000; font-size: 14px;">HOVER FOR MORE INFO</span>
                                <img src="../../images/Elections/candidate.svg" alt="" class="card-svg">
                                <div v-if="!checkCardIfHovered('candidate')" class="count">
                                    <span class="quantity">{{ electionData.number_of_candidates }}</span>
                                    <span class="quantity-label">Candidates</span>
                                </div>
                                <div v-else class="count">
                                    <div @click.prevent="fileCoc(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO FILE COC</span></div>
                                    <div @click.prevent="viewCandidates(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO VIEW CANDIDATES</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card" @mouseenter="toggleCardHover('party', 'enter')" @mouseleave="toggleCardHover('party', 'leave')">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <span v-if="!checkCardIfHovered('party')" class="quantity-label" style="color: #800000; font-size: 14px;">HOVER FOR MORE INFO</span>
                                <img src="../../images/Elections/party.svg" alt="" class="card-svg">
                                <div v-if="!checkCardIfHovered('party')" class="count">
                                    <span class="quantity">{{ electionData.number_of_partylists }}</span>
                                    <span class="quantity-label">Partylists</span>
                                </div>
                                <div v-else class="count">
                                    <div @click.prevent="registerParty(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO FILE PARTYLIST</span></div>
                                    <div @click.prevent="viewPartylists(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO VIEW PARTYLISTS</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <img src="../../images/Elections/position.svg" alt="" class="card-svg">
                                <div class="count">
                                    <span class="quantity">{{ electionData.number_of_positions }}</span>
                                    <span class="quantity-label">Positions</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <h1 class="title">Election Timeline</h1>

                <div class="timeline">
                    <div class="timeline-wrapper">
                        <ul class="timeline-line">
                            <li class="period" :class="{'active': hasStarted(electionData.election.CoCFilingStart)}">
                                <span class="period-name">FILING PERIOD</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.CoCFilingStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.CoCFilingEnd) }}</span>
                            </li>
                            <li class="period" :class="{'active': hasStarted(electionData.election.CampaignStart)}">
                                <span class="period-name">CAMPAIGN PERIOD</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.CampaignStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.CampaignEnd) }}</span>

                            </li>
                            <li class="period" :class="{'active': hasStarted(electionData.election.VotingStart)}">
                                <span class="period-name">VOTING PERIOD</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.VotingStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.VotingEnd) }}</span>
                            </li>
                            <li class="period" :class="{'active': hasStarted(electionData.election.AppealStart)}">
                                <span class="period-name">APPEAL PERIOD</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.AppealStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(electionData.election.AppealEnd) }}</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <h1 class="title" v-if="electionData.positions.length > 1">Positions</h1>
                <h1 class="title" v-else>Position</h1>

                <div class="position-set">
                    <div class="position" v-for="(position, index) in electionData.positions">
                        <div class="position-wrapper">
                            <div class="position-information">
                                <span class="quantity">{{ position.PositionQuantity }}</span>
                                <span>{{ position.PositionName }}</span>
                            </div> 
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <Appeal></Appeal>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'
    import Appeal from '../Shared/Appeal.vue'

    import axios from 'axios'
    import { ref, watch, watchEffect } from 'vue'
    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    
    export default {
        setup(props) {
            const id = ref(Number(props.id))
            const isCardHovered = ref([]);

            isCardHovered.value.push({
                id: id.value,
                candidate: false,
                party: false,
            })

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

            return {
                id,
                isCardHovered,

                electionData,
                isElectionLoading,
                isElectionSuccess,
                isElectionError,
            }
        },
        components:{
            Standards,
            Navbar,
            ActionButton,
            Appeal,
        },
        props: {
            id: '',
        },
        computed: {
    
        },
        methods:{
            returnPage(){
                router.visit('/elections')
            },
            fileCoc(election){
                if (!this.isFilingPeriod()) {
                    return alert('CoC filing for this election is currently closed.')
                }

                router.visit('/elections/view/file-coc', {
                    data: {
                        id: this.id,
                    }
                })
            },
            registerParty(election){
                if (!this.isFilingPeriod()) {
                    return alert('Partylist filing for this election is currently closed.')
                }

                router.visit('/elections/view/register-party', {
                    data: {
                        id: this.id,
                    }
                })
            },
            viewCandidates(){
                router.visit('/directory/candidates/view', {
                    data: {
                        id: this.id,
                    }
                })
            },
            viewPartylists(){
                router.visit('/directory/partylists/selection', {
                    data: {
                        id: this.id
                    }
                })
            },
            getDateTime(date){
                let getDate = new Date(date);

                let options = { 
                    month: 'long', 
                    day: 'numeric', 
                    year: 'numeric', 
                    hour: 'numeric', 
                    minute: 'numeric', 
                    hour12: true 
                };

                let formattedDate = getDate.toLocaleDateString('en-US', options);         
                
                return formattedDate;
            },
            isFilingPeriod() {
                // Check if current datetime is within filing period
                const now = new Date();
                const start = new Date(this.electionData.election.CoCFilingStart);
                const end = new Date(this.electionData.election.CoCFilingEnd);

                console.log(now => start && now < end)

                return now >= start && now < end;
            },
            isAboveVotingStartPeriod() {
                // Check if current datetime is above voting period
                const now = new Date();
                const start = new Date(this.electionData.election.VotingStart);

                return start < now;
            },
            isVotingPeriodEnded() {
                // Check if current datetime is above voting period
                const now = new Date();
                const end = new Date(this.electionData.election.VotingEnd);

                return now > end;
            },
            hasStarted(date) {
                let now = new Date();
                let start = new Date(date);

                return now >= start;
            },
            seeCandidates(){
                router.visit(`/directory/candidates/view`, {
                    data: {
                        id: this.id,
                    }
                })
            },  
            seeRankings(){
                if (!this.isAboveVotingStartPeriod()) {
                    return alert('Rankings page for this election is currently closed.')
                }

                router.visit('/elections/view/rankings', {
                    data: {
                        id: this.id,
                    }
                })
            },
            seeWinners(){
                if (!this.isVotingPeriodEnded()) {
                    return alert('Winners page for this election is currently closed.')
                }

                router.visit('/elections/view/winners', {
                    data: {
                        id: this.id,
                    }
                })
            },
            toggleCardHover(card, action){
                if (action == 'enter'){
                    this.isCardHovered[card] = true;
                }
                else if (action == 'leave'){
                    this.isCardHovered[card] = false;
                }
            },
            checkCardIfHovered(card){
                return this.isCardHovered[card]
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
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
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
        height: 50px
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
        padding: 0%;
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
        width: 100px;
    }

    .count{
        display: flex;
        flex-direction: column;
        text-align: end;
    }

    .quantity{
        font-size: 50px;
    }

    .card:hover{
        background-color: #F2F2F2;
        
        .card-svg{
            filter: invert(35%) sepia(0%) saturate(0%) hue-rotate(178deg) brightness(94%) contrast(87%);
        }
    }

    .select{
        text-decoration: none;
    }

    .select:hover{
        font-weight: bold;
        color: #9a0000;
    }

    .title{
        font-size: 22px;
        color: #800000;
        font-weight: bold;
        margin: 1.5% 0%;
    }

    .timeline{
        margin: 3% 0%;
    }

    .timeline-line{
        display: flex;
        justify-content: space-between;
        position: relative;
        padding-right: 32px;
    }

    .timeline-wrapper{
        width: 100%;
    }

    .period{
        list-style-type: none;
        width: 25%;
        position: relative;
        text-align: center;
        display: flex;
        flex-direction: column;
        flex: 1;
    }

    .period::before{
        content: " ";
        line-height: 30px;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        border: 1px solid #800000;
        display: block;
        text-align: center;
        margin: 0 auto 10px;
        background-color: white;
        z-index: 1;
    }

    .period::after{
        content: "";
        position: absolute;
        width: 100%;
        height: 2px;
        background-color: #ddd;
        top: 25px;
        left: -50%;
        z-index: 0;
    }

    .period-name{
        font-weight: bold;
    }

    .period:first-child:after{
        content: none;
    }

    .period.active{
        z-index: 1;
    }

    .period.active:before{
        border-color: #800000;
        background-color: #800000
    }

    .period.active:after{
        background-color: #800000;
    }

    .position-set{
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        justify-content: center;
    }

    .position{
        margin: 0.5% 1%;
        width: 150px;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .position-wrapper{
        padding: 2.5%;
    }

    .position-information{
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .isRankingsDisabled:disabled{
        color: #800000;
    }

    .isWinnersDisabled:disabled{
        color: #800000;
    }
</style>