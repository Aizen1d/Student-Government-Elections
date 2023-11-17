<template>
    <title>Directory View Candidates - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="scroll-up">
        <a @click="topFunction" id="mybutton">
            <img src="../../images/Directory/Candidates/scroll-up.svg" alt="" width="60px">
        </a>
    </div>

    <div class="sidebar">
        <div class="choices">
            <div class="choice">
                <div class="election-selection active">
                    {{ electionName }} 
                </div>

                <a :href="'#'+position.PositionName" v-for="(position, index) in positionsData" :key="index" class="position-selection">
                    {{ position.PositionName }}
                </a>
            </div>
        </div>
    </div>

    <div class="modal" v-if="showRateModal">
        <div class="modal-content" v-if="isVerified">
            <div class="row" style="margin-top: -2%;">
                <div class="col-10">
                    <p style="margin-top: 2%; margin-left: 35%;"><b>Rate Candidates</b> (Verify first before rating)</p>
                </div>
                <div class="col-2" style="text-align: end;">
                    <span class="close" @click="closeRateCandidates">&times;</span>
                </div>
            </div>

            <div class="row" style="margin-top: 3%;">
                <div class="col-6" style="">
                    <input type="text" style="width: 80%; margin-left: 23%;" class="form-control" maxlength="15" placeholder="Enter your student number" v-model="student_number">
                </div>
                <div class="col-6">
                <ActionButton @click.prevent="sendCode" :disabled="isSending || isSent || student_number === ''" 
                                    :style="{ width: isSent ? '20em' : '15em' }"
                                    style="font-size: 1em;
                                    margin-left: 3%;
                                    height: 2.2em; 
                                    padding: 0px 0px 0px 0px !important;">{{ buttonText }}</ActionButton>
                </div>
            </div>

            <div class="row" style="margin-top: 3%;">
                <div class="col-6" style="">
                    <input type="text" style="width: 80%; margin-left: 23%;" class="form-control" placeholder="Enter your verification code" v-model="verification_code">
                </div>
                <div class="col-6">
                <ActionButton class="verify-button" @click.prevent="verify" :disabled="isVerifying || verification_code === ''" 
                                    :style="{ width: '15em' }"
                                    style="font-size: 1em;
                                    margin-left: 3%;
                                    height: 2.2em; 
                                    padding: 0px 0px 0px 0px !important;">Verify</ActionButton>
                </div>
            </div>
        </div>

        <div class="modal-content" v-else>
            <div class="row" style="margin-top: -2%;">
                <div class="col-10">
                    <p style="margin-top: 2%; margin-left: 35%;"><b>Rate Candidates</b> (One time only)</p>
                </div>
                <div class="col-2" style="text-align: end;">
                    <span class="close" @click="closeRateCandidates">&times;</span>
                </div>
            </div>

            <div class="row" style="margin-top: -1%;" v-for="(position, positionIndex) in positionsData" :key="positionIndex">
                <h1 class="rate-position-name">{{ position.PositionName }}</h1>
                <div class="col-8" style="display: flex;" v-for="(candidate, candidateIndex) in candidatesData" :key="candidateIndex">
                    <template v-if="candidate.SelectedPositionName === position.PositionName">
                        <h1 class="rate-candidate-name">
                            {{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}
                        </h1>
                        <div class="rate" style="margin-top: -2.5%; !important">
                            <input type="radio" :id="'star5-' + positionIndex + '-' + candidateIndex" :name="'rate-' + positionIndex + '-' + candidateIndex" value="5"/>
                            <label :for="'star5-' + positionIndex + '-' + candidateIndex" title="text">5 stars</label>
                            
                            <input type="radio" :id="'star4-' + positionIndex + '-' + candidateIndex" :name="'rate-' + positionIndex + '-' + candidateIndex" value="4" />
                            <label :for="'star4-' + positionIndex + '-' + candidateIndex" title="text">4 stars</label>

                            <input type="radio" :id="'star3-' + positionIndex + '-' + candidateIndex" :name="'rate-' + positionIndex + '-' + candidateIndex" value="3" />
                            <label :for="'star3-' + positionIndex + '-' + candidateIndex" title="text">3 stars</label>

                            <input type="radio" :id="'star2-' + positionIndex + '-' + candidateIndex" :name="'rate-' + positionIndex + '-' + candidateIndex" value="2" />
                            <label :for="'star2-' + positionIndex + '-' + candidateIndex" title="text">2 stars</label>

                            <input type="radio" :id="'star1-' + positionIndex + '-' + candidateIndex" :name="'rate-' + positionIndex + '-' + candidateIndex" value="1" />
                            <label :for="'star1-' + positionIndex + '-' + candidateIndex" title="text">1 star</label>
                        </div>
                    </template>
                </div>

                <div class="col-4">
                    
                </div>
                <hr>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="row" style="margin-left: 1.8%; margin-top: 5%; margin-right: 2%; margin-bottom: -3%;">
            <div class="col-10">
                <h1 class="eligible">
                    <span class="return" @click="returnDirectory">Directory</span>&nbsp;>&nbsp;<span class="return" @click="returnSelection">Election Selection</span>&nbsp;>&nbsp;{{ activeElectionName }}
                </h1>
            </div>
            <div class="col-2" style="text-align: end;">
                <ActionButton class="col-2 rate-button" @click="openRateCandidates">Rate Candidates</ActionButton>
            </div>
        </div>

        <h2 style="margin-top: 4%; margin-left: 2.6%;" v-if="isCandidatesLoading">Loading..</h2>

        <template v-for="(position, index) in positionsData" :key="index">
            <div class="position row">
                <h1 :id="position.PositionName" class="col-10">{{ position.PositionName }} Candidates</h1>
                <hr class="my-4">

                <div class="candidate" v-for="(candidate, index) in candidatesData">
                    <div v-if="candidate.SelectedPositionName === position.PositionName">
                        <table>
                            <tbody>
                                <tr>
                                    <td>
                                        <img :src="candidate.DisplayPhoto" class="cpic" alt="">
                                    </td>
                                    <td class="info">
                                        <div class="data">
                                            <div class="align">
                                                <div class="name">
                                                    <strong>
                                                        {{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}
                                                    </strong>
                                                </div>
                                                <div class="rate">
                                                    <input type="radio" id="star5" name="rate" value="5" />
                                                    <label for="star5" title="text">5 stars</label>
                                                    <input type="radio" id="star4" name="rate" value="4" />
                                                    <label for="star4" title="text">4 stars</label>
                                                    <input type="radio" id="star3" name="rate" value="3" />
                                                    <label for="star3" title="text">3 stars</label>
                                                    <input type="radio" id="star2" name="rate" value="2" />
                                                    <label for="star2" title="text">2 stars</label>
                                                    <input type="radio" id="star1" name="rate" value="1" />
                                                    <label for="star1" title="text">1 star</label>
                                                </div>
                                            </div>
                                            <div class="affiliation">{{ candidate.PoliticalAffiliation }}: {{ candidate.PartyListName }}</div>
                                        </div>

                                        <div class="quote">
                                            <em>"{{ candidate.Motto }}"</em>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </template>
    
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed, watchEffect, watch } from 'vue';
    import { useLocalStorage } from '@vueuse/core';
    import axios from 'axios';

    export default {
        setup(props) {
            const activeElectionIndex = ref(Number(props.id));
            const activeElectionName = ref(props.electionName);
            const atLeastOneCandidate = ref(false);

            const showRateModal = ref(false);

            const student_number = ref('');
            const verification_code = useLocalStorage(`rating_verification_code_${activeElectionIndex.value}`, '')
            const isSending = useLocalStorage(`rating_is_sending_${activeElectionIndex.value}`, false);
            const isSent = useLocalStorage(`rating_is_sent_${activeElectionIndex.value}`, false);
            const countdown = useLocalStorage(`rating_countdown${activeElectionIndex.value}`, 0);

            const isVerifying = ref(false);
            const isVerified = useLocalStorage(`rating_is_verified_${activeElectionIndex.value}`, false);

            // For Sidebar data
            const fetchElections = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`);
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                return response.data.elections;
            }

            const { data: electionsData,
                isLoading: isElectionsLoading,
                isSuccess: isElectionsSuccess,
                isError: isElectionsError } =
                useQuery({
                    queryKey: ['fetchElections'],
                    queryFn: fetchElections,
                })

            // For fetching positions from selected election
            const fetchPositionsOnElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${activeElectionIndex.value}`);
                console.log(`Get all positions from selected election successful. Duration: ${response.duration}ms`)

                return response.data.positions;
            }

            const { data: positionsData,
                isLoading: isPositionsLoading,
                isSuccess: isPositionsSuccess,
                isError: isPositionsError,
                isRefetching: isPositionsRefetching,
                refetch: positionsRefetch } =
                useQuery({
                    queryKey: [`fetchPositionsOnElection${activeElectionIndex.value}`],
                    queryFn: fetchPositionsOnElection,
                })
            
            // For fetching candidates from selected election
            const fetchCandidatesFromSelectedElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/${activeElectionIndex.value}/approved/coc/all`);
                console.log(`Get all candidates from selected election successful. Duration: ${response.duration}ms`)

                if (response.data.cocs.length > 0) {
                    atLeastOneCandidate.value = true;
                }
                else {
                    atLeastOneCandidate.value = false;
                }

                return response.data.cocs;
            }

            const { data: candidatesData,
                isLoading: isCandidatesLoading,
                isSuccess: isCandidatesSuccess,
                isError: isCandidatesError,
                isRefetching: isCandidatesRefetching,
                refetch: candidatesRefetch } =
                useQuery({
                    queryKey: [`fetchCandidatesFromSelectedElection${activeElectionIndex.value}`],
                    queryFn: fetchCandidatesFromSelectedElection,
                })

            return {
                activeElectionIndex,
                activeElectionName,
                atLeastOneCandidate,

                showRateModal,
                student_number,
                verification_code,
                isSending,
                isSent,
                countdown,
                isVerifying,
                isVerified,

                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,

                positionsData,
                isPositionsLoading,
                isPositionsSuccess,
                isPositionsError,
                isPositionsRefetching,

                candidatesData,
                isCandidatesLoading,
                isCandidatesSuccess,
                isCandidatesError,
                isCandidatesRefetching,

                fetchElections,
                fetchPositionsOnElection,
                fetchCandidatesFromSelectedElection,
            }
        },
        components: {
            Standards,
            Navbar,
            ActionButton
        },
        props: {
            id: '',
            electionName: ''
        },
        computed: {
            buttonText() {
                if (this.isSending) {
                    return 'Sending..';
                }
                else if (this.isSent) {
                    return `Resend in ${this.countdown} seconds`;
                }
                else {
                    return 'Send Code';
                }
            },
        },
        methods: {
            returnDirectory() {
                router.visit('/directory')
            },
            returnSelection() {
                router.visit('/directory/candidates')
            },
            toggleElection(index) {
                this.activeElectionIndex = this.activeElectionIndex === index ? null : index;
            },
            openRateCandidates() {
                this.showRateModal = true;
            },
            closeRateCandidates() {
                this.showRateModal = false;
            },
            sendCode() {
                if (this.student_number === '') {
                    return alert('Please enter your student number.')
                } 

                this.isSending = true;

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/code/ratings/verification/generate`, {
                    student_number: this.student_number,
                    code_type: 'Rating-Verification'
                })
                .then((response) => {
                    // console.log(response) // commented out because code can be seen in the console
                    alert(`Verification code sent to your email ${response.data.email_address}`)

                    this.isSending = false;
                    this.isSent = true;
                    this.countdown = 30; // seconds
                    this.intervalId = setInterval(() => {
                        if (this.countdown > 1) {
                            this.countdown--;
                        } 
                        else {
                            clearInterval(this.intervalId);
                            this.isSent = false;
                        }
                    }, 1000);
                })
                .catch((error) => {
                    console.log(error)

                    alert('Student number does not exist.') 
                    this.isSending = false;
                })
            },
            verify() {
                if (this.verification_code === '') {
                    return alert('Please enter your verification code.')
                }

                this.isVerifying = true;

                const code_type = 'Rating-Verification';

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/code/ratings/verify/${this.verification_code}/${code_type}`)
                .then((response) => {
                    // console.log(response) // commented out because code can be seen in the console
                    if (response.data.valid) {
                        alert('Verification successful!')
                    }
                })
                .catch((error) => {
                    console.log(error)

                    alert('Code does not exist or has expired.')
                })
                .finally(() => {
                    this.isVerifying = false;
                })

            }
         }
    }
</script>

<style scoped>
    .modal {
        display: block; /* Hidden by default */
        position: fixed; /* Stay in place */
        z-index: 1; /* Sit on top */
        padding-top: 100px; /* Location of the box */
        left: 0;
        top: 0;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgb(0,0,0); /* Fallback color */
        background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    }

        /* Modal Content */
    .modal-content {
        background-color: #fefefe;
        margin: auto;
        padding: 20px;
        border: 1px solid #888;
        width: 40%;
    }

        /* The Close Button */
    .close {
        color: #000;
        font-size: 29px;
        font-weight: bold;
        margin-top: -2%;
        width: fit-content;
    }

    .close:hover {
        text-decoration: none;
        cursor: pointer;
    }

    .rate-position-name{
        font-size: 28px;
        font-weight: 800;
        color: #B90321;
        margin-bottom: 2%;
    }

    .rate-candidate-name{
        font-size: 22px;
        font-weight: normal;
        margin-bottom: 2%;
        margin-right: 2%;
        margin-left: 7%;
    }

    .rate-input{
        width: 10%;
        height: 80%;
        text-align: center;
        font-size: 20px;
        font-weight: 800;
    }

    .eligible{
        font-size: 28px;
        font-weight: 800;
    }

    .return{
        font-size: 28px;
        font-weight: 800;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .election-selection{
        background-color: transparent;
        border: none;
        color: black;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 2%;
        font-family: 'Source Sans Pro Black', sans-serif !important;
    }

    .election-selection:hover{
        color: #CA2B00;
        cursor: pointer;
    }

    .position-selection {
        background-color: transparent;
        border: none;
        color: black;
        margin-left: 12%;
        font-size: 18px;
        padding-bottom: 3%;
        font-family: 'Source Sans Pro Black', sans-serif !important;
        display: flex;
        text-decoration: none;
        transition: padding-left .3s ease;
    }

    .position-selection:hover {
        cursor: pointer;
        color: #CA2B00;
        padding-left: 15px;
    }

    .active {
        color: #CA2B00;
    }

    .slide-fade-enter-active {
        transition: all .3s ease;
    }
    .slide-fade-leave-active {
        transition: all .2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
    }
    .slide-fade-enter, .slide-fade-leave-to {
        transform: translateX(10px);
        opacity: 0;
    }

    .sidebar {
        height: 100%;
        /* Full-height: remove this if you want "auto" height */
        width: 300px;
        /* Set the width of the sidebar */
        position: fixed;
        /* Fixed Sidebar (stay in place on scroll) */
        top: 1;
        left: 0;
        overflow-x: hidden;
        /* Disable horizontal scroll */
        padding-top: 1.5%;
        font-family: 'Source Sans Pro', sans-serif;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    }

    .choices {
        text-align: start;
        margin: 0% 10%;
    }

    .choices h1 {
        color: #9A000A;
        font-size: 30px;
        font-weight: 900;
    }

    .options {
        margin: 0%;
        margin-top: 10%;
        display: grid;
    }

    .options a {
        margin: 3% 0%;
        text-decoration: none;
        color: black;
        font-size: 18px;
    }

    .main {
        margin-left: 300px;
        font-family: 'Source Sans Pro', sans-serif;
        margin-top: -2.7%;
    }

    .position {
        margin: 5% 2%;
    }

    .position h1 {
        color: #9A000A;
        font-size: 29px;
        font-weight: 700;
        margin: 0%;
    }

    .rate-button {
        padding: 4%;
        width: 85%;
    }

    .candidate {
        width: 100%;
    }

    .cpic {
        width: 320px;
        height: 440px;
        object-fit: cover;
    }

    .info {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 22px;
        width: 100%;
        padding: 0% 2%;
    }

    .align {
        display: flex;
        align-items: center;
    }

    .quote {
        text-align: center;
        margin-top: 50px;
    }

    .candidate:hover {
        color: #CA2B00;
    }

    .candidate td {
        vertical-align: top;
    }

    .scroll-up {
        display: block;
        position: fixed;
        /* Fixed/sticky position */
        bottom: 100px;
        /* Place the button at the bottom of the page */
        right: 110px;
        /* Place the button 30px from the right */
        z-index: 99;
        /* Make sure it does not overlap */
        filter: invert(12%) sepia(37%) saturate(6821%) hue-rotate(344deg) brightness(105%) contrast(119%);
    }

    .scroll-up:hover {
        filter: invert(86%) sepia(41%) saturate(799%) hue-rotate(354deg) brightness(93%) contrast(97%);
    }

    .rate {
        height: 46px;
        padding: 0 10px;
    }

    .rate:not(:checked)>input {
        position: absolute;
        top: -9999px;
    }

    .rate:not(:checked)>label {
        float: right;
        width: 1em;
        overflow: hidden;
        white-space: nowrap;
        cursor: pointer;
        font-size: 30px;
        color: #ccc;
    }

    .rate:not(:checked)>label:before {
        content: '★ ';
    }

    .rate>input:checked~label {
        color: #EEB503;
    }

    .rate:not(:checked)>label:hover,
    .rate:not(:checked)>label:hover~label {
        color: #dfa804;
    }

    .rate>input:checked+label:hover,
    .rate>input:checked+label:hover~label,
    .rate>input:checked~label:hover,
    .rate>input:checked~label:hover~label,
    .rate>label:hover~input:checked~label {
        color: #c59b08;
    }
</style>