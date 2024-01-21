<template>
    <title>Elections - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="header">ONGOING ELECTIONS</h1>

        <div class="election" v-for="(election, index) in electionsData" v-if="isElectionsSuccess">
            <div class="election-wrapper" :class="{ 'open': isOpen(election.ElectionId) }">
                <div class="election-header">
                    <div class="centered">
                        <img :src="election.OrganizationLogo" alt="" class="election-logo">
                        <span class="election-title">{{ election.ElectionName }}</span>
                            <button class="view-button" @click.prevent="viewMore(election)" v-if="isOpen(election.ElectionId)">
                                <img src="../../images/Elections/view.svg" alt="" class="view-svg"> 
                                View more details
                            </button>
                        <div class="end">
                            <button class="down-button" @click.prevent="toggleElectionCard(election)">
                                <img src="../../images/Elections/down.svg" alt="" class="down-svg" :class="{ 'rotate-up': isOpen(election.ElectionId), 'rotate-down': !isOpen(election.ElectionId) }">
                            </button>
                        </div>
                    </div>
                </div>
                
                <hr :class="isOpen(election.ElectionId) ? 'line' : 'line-hidden'">

                <div class="card-set">
                    <div class="card" @mouseenter="toggleCardHover(election, 'candidate', 'enter')" @mouseleave="toggleCardHover(election, 'candidate', 'leave')">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <span v-if="!checkCardIfHovered(election, 'candidate')" class="quantity-label" style="color: #800000; font-size: 14px;">HOVER FOR MORE INFO</span>
                                <img src="../../images/Elections/candidate.svg" alt="" class="card-svg">
                                <div v-if="!checkCardIfHovered(election, 'candidate')" class="count">
                                    <span class="quantity">{{ election.NumberOfCandidates }}</span>
                                    <span class="quantity-label">Candidates</span>
                                </div>
                                <div v-else class="count">
                                    <div @click.prevent="fileCoc(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO FILE COC</span></div>
                                    <div @click.prevent="viewCandidates(election)" style="cursor: pointer; font-size: 14px;" class="select"><span class="action"> CLICK TO VIEW CANDIDATES</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card" @mouseenter="toggleCardHover(election, 'party', 'enter')" @mouseleave="toggleCardHover(election, 'party', 'leave')">
                        <div class="card-wrapper">
                            <div class="card-information">
                                <span v-if="!checkCardIfHovered(election, 'party')" class="quantity-label" style="color: #800000; font-size: 14px;">HOVER FOR MORE INFO</span>
                                <img src="../../images/Elections/party.svg" alt="" class="card-svg">
                                <div v-if="!checkCardIfHovered(election, 'party')" class="count">
                                    <span class="quantity">{{ election.NumberOfPartylists }}</span>
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
                                    <span class="quantity">{{ election.NumberOfPositions }}</span>
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
                            <li class="period" :class="{'active': hasStarted(election.CoCFilingStart)}">
                                <span class="period-name">FILING PERIOD</span>
                                <span class="period-dates">{{ getDateTime(election.CoCFilingStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(election.CoCFilingEnd) }}</span>
                            </li>
                            <li class="period" :class="{'active': hasStarted(election.CampaignStart)}">
                                <span class="period-name">CAMPAIGN PERIOD</span>
                                <span class="period-dates">{{ getDateTime(election.CampaignStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(election.CampaignEnd) }}</span>

                            </li>
                            <li class="period" :class="{'active': hasStarted(election.VotingStart)}">
                                <span class="period-name">VOTING PERIOD</span>
                                <span class="period-dates">{{ getDateTime(election.VotingStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(election.VotingEnd) }}</span>
                            </li>
                            <li class="period" :class="{'active': hasStarted(election.AppealStart)}">
                                <span class="period-name">APPEAL PERIOD</span>
                                <span class="period-dates">{{ getDateTime(election.AppealStart) }}</span>
                                <span class="period-dates">to</span>
                                <span class="period-dates">{{ getDateTime(election.AppealEnd) }}</span>
                            </li>
                        </ul>
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
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'
    import Appeal from '../Shared/Appeal.vue'

    import { ref } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'
    import { useLocalStorage } from '@vueuse/core'

    export default {
        setup(props){
            const showElection = ref([]);
            const isCardHovered = ref([]);

            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`, {
                });
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                // save the state if open or not (dropdown) in showElection, include the election id and state
                response.data.elections.forEach((election) => {
                    showElection.value.push({
                        id: election.ElectionId,
                        open: false,
                    })

                    isCardHovered.value.push({
                        id: election.ElectionId,
                        candidate: false,
                        party: false,
                    })
                })

                return response.data.elections.map(election => {
                    const logo_url = `${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/get/cached/elections/${election.OrganizationLogo}`
                    election.OrganizationLogo = logo_url;

                    return election;
                });
            }

            const { data: electionsData,
                    isLoading: isElectionsLoading,
                    isSuccess: isElectionsSuccess,
                    isError: isElectionsError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            const isOpen = (id) => {
                const election = showElection.value.find(e => e.id === id);
                return election ? election.open : false;
            };

            return{
                showElection,
                isCardHovered,

                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,

                isOpen,
            }
        },
        components:{
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
            Appeal,
        },
        methods:{
            viewMore(election){
                router.visit('/elections/view', {
                    data: {
                        id: election.ElectionId,
                    }
                })
            },
            fileCoc(election){
                if (!this.isFilingPeriod(election)) {
                    return alert('CoC filing for this election is currently closed.')
                }

                router.visit('/elections/view/file-coc', {
                    data: {
                        id: election.ElectionId,
                    }
                })
            },
            registerParty(election){
                if (!this.isFilingPeriod(election)) {
                    return alert('Partylist filing for this election is currently closed.')
                }

                router.visit('/elections/view/register-party', {
                    data: {
                        id: election.ElectionId,
                    }
                })
            },
            viewCandidates(election){
                router.visit('/directory/candidates/view', {
                    data: {
                        id: election.ElectionId,
                    }
                })
            },
            viewPartylists(election){
                router.visit('/directory/partylists/selection', {
                    data: {
                        id: election.ElectionId,
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
            isFilingPeriod(election) {
                // Check if current datetime is within filing period
                const now = new Date();
                const start = new Date(election.CoCFilingStart);
                const end = new Date(election.CoCFilingEnd);

                console.log(now => start && now < end)

                return now >= start && now < end;
            },
            hasStarted(date) {
                let now = new Date();
                let start = new Date(date);

                return now >= start;
            },
            toggleElectionCard(election){
                const index = this.showElection.findIndex(e => e.id === election.ElectionId);
                this.showElection[index].open = !this.showElection[index].open;
            },
            toggleCardHover(election, card, action){
                const index = this.isCardHovered.findIndex(e => e.id === election.ElectionId);
                
                if (action === 'enter'){
                    this.isCardHovered[index][card] = true;
                }
                else if (action === 'leave'){
                    this.isCardHovered[index][card] = false;
                }
            },
            checkCardIfHovered(election, card){
                // Make sure election card is open
                if (!this.isOpen(election.ElectionId)) {
                    return;
                }

                const index = this.isCardHovered.findIndex(e => e.id === election.ElectionId);
                return this.isCardHovered[index][card]
            },
        },
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
        font-family: 'Inter', sans-serif;
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
        height: 50px;
        object-fit: cover;
    }

    .election-title{
        font-size: 30px;
        font-weight: bold;
        color: #800000;
        margin: 0% 1.5%;
        font-family: 'Inter', sans-serif;
    }

    .view-svg{
        width: 23px;
        margin-right: 5px;
    }

    .view-button{
        border: transparent;
        background-color: transparent;
        display: flex;
        align-items: center;
    }

    .view-button:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .down-svg{
        width: 20px;
    }

    .down-button{
        border: transparent;
        background-color: transparent;
        display: flex;
        align-items: center;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .line-hidden{
        border: 0;
        height: 0px;
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
        margin-top: 3%;
    }

    .timeline-line{
        display: flex;
        justify-content: space-between;
        position: relative;
        padding-right: 32px;
    }

    .timeline-wrapper{
        width: 100%
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

    @keyframes bounceEase {
        0% { transform: translateY(0); }
        20% { transform: translateY(-15px); }
        40% { transform: translateY(5px); }
        60% { transform: translateY(-5px); }
        80% { transform: translateY(2px); }
        100% { transform: translateY(0); }
    }

    .election-wrapper {
        transition: max-height 0.3s ease-in-out;
        max-height: 120px;
        overflow: hidden;
    }

    .election-wrapper.open {
        max-height: 600px;
        animation: bounceEase 1s ease-in-out forwards;
    }

    .rotate-up{
        transition: 0.3s ease-in-out;
        transform: rotate(180deg);
    }

    .rotate-down{
        transition: 0.3s ease-in-out;
        transform: rotate(360deg);
    }
</style>