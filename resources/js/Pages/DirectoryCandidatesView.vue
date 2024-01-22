<template>
    <title>Directory View Candidates - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnDirectory">Directory</span> 
            <span class="arrow"> > Candidates ></span>
            <span class="arrow return-selection" @click.prevent="returnSelection"> Select Election</span>
            
            <span class="arrow"> ></span>
            View Candidates
        </h1>
         
        <div class="modal" v-if="showRateModal">
            <div class="candidate-rating modal-content">
                <div class="candidate-rating-wrapper" v-if="!isVerified">
                    <div class="verification">
                        <div class="verification-header">
                            <h1 class="header-label">Candidate Rating Verification</h1>
                            <Tooltip class="mx-3">
                                <slot>
                                    To rate candidates, submit your student number. An email with a verification code will be sent to your associated email. Use this code to verify.
                                </slot>
                            </Tooltip>
                            <button class="close-button" @click="closeRateCandidates"><img src="../../images/Directory/Candidates/View/close.svg" alt="" class="close-svg"></button>
                        </div>
                        <span class="warning"><strong>Note</strong>: You can rate only once.</span>

                        <hr class="line">

                        <div class="inputs row">
                            <label class="form-label" for="student-number">Student Number</label>
                            <div class="col-8">
                                <input class="form-control" type="text" name="student-number" maxlength="15" placeholder="Enter your student number" v-model="student_number">
                            </div>
                            <div class="col-4">
                                <button class="code-button disabled-button" @click.prevent="sendCode" :disabled="isSending || isSent || student_number === ''" >{{ buttonText }}</button>
                            </div>

                            <div>
                                <label class="form-label margin mt-4" for="code">Verification Code</label>
                                <input class="form-control" type="text" name="code" placeholder="Enter your verification code" v-model="verification_code">
                            </div>

                            <div class="verify">
                                <button class="verify-button disabled-button" @click.prevent="verify" :disabled="isVerifying || verification_code === ''">Verify</button>
                            </div>
                        </div>
                    </div>
                </div>
        
                <div class="candidate-rating-wrapper" v-else>
                    <div class="verification" v-for="(position, positionIndex) in positionsData" :key="positionIndex">
                        <div class="verification-header">
                            <h1 class="header-label">Candidate Rating Verification</h1>
                            <button class="close-button" @click="closeRateCandidates"><img src="../../images/Directory/Candidates/View/close.svg" alt="" class="close-svg"></button>
                        </div>

                        <template v-for="(candidate, candidateIndex) in candidatesData" :key="candidateIndex">
                            <template v-if="candidate.SelectedPositionName === position.PositionName">
                                <hr class="line">

                                <div class="inputs row">
                                    <span class="position-title" style="color: #800000;">{{ position.PositionName }}</span>
                                    <div class="rating">
                                        <div class="rate-candidate">
                                            <input type="radio" :id="'candidate-star5-' + positionIndex + '-' + candidateIndex" :name="'candidate-rate-' + positionIndex + '-' + candidateIndex" value="5"/>
                                            <label :for="'candidate-star5-' + positionIndex + '-' + candidateIndex" title="text">5 stars</label>
                                            
                                            <input type="radio" :id="'candidate-star4-' + positionIndex + '-' + candidateIndex" :name="'candidate-rate-' + positionIndex + '-' + candidateIndex" value="4" />
                                            <label :for="'candidate-star4-' + positionIndex + '-' + candidateIndex" title="text">4 stars</label>

                                            <input type="radio" :id="'candidate-star3-' + positionIndex + '-' + candidateIndex" :name="'candidate-rate-' + positionIndex + '-' + candidateIndex" value="3" />
                                            <label :for="'candidate-star3-' + positionIndex + '-' + candidateIndex" title="text">3 stars</label>

                                            <input type="radio" :id="'candidate-star2-' + positionIndex + '-' + candidateIndex" :name="'candidate-rate-' + positionIndex + '-' + candidateIndex" value="2" />
                                            <label :for="'candidate-star2-' + positionIndex + '-' + candidateIndex" title="text">2 stars</label>

                                            <input type="radio" :id="'candidate-star1-' + positionIndex + '-' + candidateIndex" :name="'candidate-rate-' + positionIndex + '-' + candidateIndex" value="1" />
                                            <label :for="'candidate-star1-' + positionIndex + '-' + candidateIndex" title="text">1 star</label>
                                        </div>
                                        <span class="candidate-name">{{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}</span>
                                        <span class="candidate-info" v-if="candidate.PartyListName">{{ candidate.PartyListName }}</span>
                                        <span class="candidate-info" v-else>Independent</span>
                                        <span class="candidate-info">{{ candidate.Student.CourseCode }} {{ candidate.Student.Year }}-{{ candidate.Student.Section }}</span>
                                    </div>
                                </div>

                            </template>
                        </template>

                    </div>

                    <hr class="line">
                    
                    <div class="verify">
                        <button class="verify-button" @click="submitRating">Submit</button>
                    </div>
                </div>
            </div>
        </div>

        <h1 v-if="isElectionsLoading && isPositionsLoading && isCandidatesLoading && isCandidatesPerPositionLoading">Loading..</h1>
        <div v-if="!isElectionsLoading && !isPositionsLoading && !isCandidatesLoading && !isCandidatesPerPositionLoading" class="election">
            <div class="election-wrapper">
                <div class="election-header">
                    <div class="centered">
                        <img src="" alt="" class="election-logo">
                        <span class="election-title">{{ electionName }}</span>
                        <div class="end">
                            <button class="header-button" @click="fileCoc"><img src="../../images/Directory/Candidates/View/file-coc.svg" alt="" class="header-svg"></button>
                            <button class="header-button space" @click="openRateCandidates" :disabled="isCandidatesPerPositionLoading || !isCampaignPeriod || !atLeastOneCandidate"><img src="../../images/Directory/Candidates/View/rate.svg" alt="" class="header-svg result"></button>
                        </div>
                    </div>
                </div>

                <hr class="line">

                <div class="candidate-list">
                    <aside class="position-sidebar">
                        <h1 class="position-label">POSITIONS</h1>

                        <a :href="'#'+position.PositionName" v-if="atLeastOneCandidate === true" v-for="(position, index) in positionsData" :key="index" 
                            class="select-position">
                            <span class="position">{{ position.PositionName }}</span>
                        </a>
                    </aside>

                    <div class="candidate-content" v-if="!isCandidatesPerPositionLoading" v-for="(candidatePosition, candidatePositionName, candidatePositionIndex) in candidatesPerPositionData" :key="candidatePositionIndex">
                        <div class="mt-1 mb-3" style="text-align: center;">
                            <span :id="candidatePositionName" class="position-title" style="color: #800000; text-transform: uppercase;">{{ candidatePositionName }} Candidates</span>
                        </div>
                        <div class="candidate" v-if="candidatePosition.length > 0" v-for="(candidate, candidateIndex) in candidatePosition">
                            <div class="candidate-wrapper">
                                <div class="candidate-information">
                                    <img :src="candidate.DisplayPhoto" alt="" class="candidate-img">
                                    <div class="candidate-description">
                                        <div class="spacing">
                                            <span class="candidate-name">{{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}</span>
                                            <span v-if="candidate.Rating && candidate.TimesRated">Ratings: {{ candidate.Rating / candidate.TimesRated }}</span>
                                            <span v-else>Ratings: 0</span>
                                            <div class="rate-candidate">
                                                <input type="radio" :id="'star5-' + candidatePositionIndex + '-' + candidateIndex" :name="'rate-' + candidatePositionIndex + '-' + candidateIndex" value="5"
                                                        :checked="candidate.Rating / candidate.TimesRated >= 5" disabled/>
                                                <label :for="'star5-' + candidatePositionIndex + '-' + candidateIndex" title="5 star">5 stars</label>
                                                
                                                <input type="radio" :id="'star4-' + candidatePositionIndex + '-' + candidateIndex" :name="'rate-' + candidatePositionIndex + '-' + candidateIndex" value="4" 
                                                        :checked="candidate.Rating / candidate.TimesRated >= 4 && candidate.Rating / candidate.TimesRated <= 4.99" disabled/>
                                                <label :for="'star4-' + candidatePositionIndex + '-' + candidateIndex" title="4 star">4 stars</label>

                                                <input type="radio" :id="'star3-' + candidatePositionIndex + '-' + candidateIndex" :name="'rate-' + candidatePositionIndex + '-' + candidateIndex" value="3" 
                                                        :checked="candidate.Rating / candidate.TimesRated >= 3 && candidate.Rating / candidate.TimesRated <= 3.99" disabled/>
                                                <label :for="'star3-' + candidatePositionIndex + '-' + candidateIndex" title="3 star">3 stars</label>

                                                <input type="radio" :id="'star2-' + candidatePositionIndex + '-' + candidateIndex" :name="'rate-' + candidatePositionIndex + '-' + candidateIndex" value="2" 
                                                        :checked="candidate.Rating / candidate.TimesRated >= 2 && candidate.Rating / candidate.TimesRated <= 2.99" disabled/>
                                                <label :for="'star2-' + candidatePositionIndex + '-' + candidateIndex" title="2 star">2 stars</label>

                                                <input type="radio" :id="'star1-' + candidatePositionIndex + '-' + candidateIndex" :name="'rate-' + candidatePositionIndex + '-' + candidateIndex" value="1" 
                                                        :checked="candidate.Rating / candidate.TimesRated >= 1 && candidate.Rating / candidate.TimesRated <= 1.99" disabled/>
                                                <label :for="'star1-' + candidatePositionIndex + '-' + candidateIndex" title="1 star">1 stars</label>
                                            </div>
                                        </div>
                                        <span class="etc" v-if="candidate.PartyListName">{{ candidate.PartyListName }}</span>
                                        <span class="etc" v-else>Independent</span>
                                        <span class="etc">{{ candidate.Student.CourseCode }} {{ candidate.Student.Year }}-{{ candidate.Student.Section }}</span>
                                        <span class="motto" v-if="candidate.Motto && candidate.Motto !== ''">“{{ candidate.Motto }}”</span>
                                        <span class="motto" v-else>No motto for this candidate.</span>

                                        <span class="platform-label">Platform:</span>
                                        <p class="platform">
                                            {{ candidate.Platform }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <br>
    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'
    import Tooltip from '../Shared/Tooltip.vue';

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed, watchEffect, watch } from 'vue';
    import { useLocalStorage } from '@vueuse/core';
    import axios from 'axios';

    export default {
        setup(props) {
            const activeElectionIndex = ref(Number(props.id));
            const activeElectionName = ref(props.electionName);
            const atLeastOneCandidate = ref(null);

            const showRateModal = ref(false);

            const student_number = ref('');
            const rater_student_number = ref(''); 

            const verification_code = ref('');
            const isSending = useLocalStorage(`rating_is_sending_${activeElectionIndex.value}`, false);
            const isSent = useLocalStorage(`rating_is_sent_${activeElectionIndex.value}`, false);
            const countdown = useLocalStorage(`rating_countdown${activeElectionIndex.value}`, 0);

            const isVerifying = ref(false);
            const isVerified = ref(false);

            const fetchActiveElection = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${activeElectionIndex.value}`);
                console.log(`Get election with id ${activeElectionIndex.value} successful. Duration: ${response.duration}ms`)

                return response.data.election;
            }

            const { data: electionsData,
                isLoading: isElectionsLoading,
                isSuccess: isElectionsSuccess,
                isError: isElectionsError } =
                useQuery({
                    queryKey: [`fetchActiveElection-${activeElectionIndex.value}`],
                    queryFn: fetchActiveElection,
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
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/candidates/election/${activeElectionIndex.value}/all`);
                console.log(`Get all candidates from selected election successful. Duration: ${response.duration}ms`)

                return response.data.candidates;
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

            const fetchCandidatsPerSelectedPosition = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/candidates/election/per-position/${activeElectionIndex.value}/all`);
                console.log(`Get all candidates from selected election successful. Duration: ${response.duration}ms`)

                let hasCandidates = false;
                for (let position in response.data.candidates) {
                    if (response.data.candidates[position].length > 0) {
                    hasCandidates = true;
                    break;
                    }
                }

                if (hasCandidates) {
                    atLeastOneCandidate.value = true;
                } 
                else {
                    atLeastOneCandidate.value = false;
                }

                return response.data.candidates;
            }

            const { data: candidatesPerPositionData,
                isLoading: isCandidatesPerPositionLoading,
                isSuccess: isCandidatesPerPositionSuccess,
                isError: isCandidatesPerPositionError,
                isRefetching: isCandidatesPerPositionRefetching, } =
                useQuery({
                    queryKey: [`fetchCandidatsPerSelectedPosition${activeElectionIndex.value}`],
                    queryFn: fetchCandidatsPerSelectedPosition,
                })

            return {
                activeElectionIndex,
                activeElectionName,
                atLeastOneCandidate,

                showRateModal,
                student_number,
                rater_student_number,
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

                candidatesPerPositionData,
                isCandidatesPerPositionLoading,
                isCandidatesPerPositionSuccess,
                isCandidatesPerPositionError,
                isCandidatesPerPositionRefetching,

                fetchPositionsOnElection,
                fetchCandidatesFromSelectedElection,
                fetchCandidatsPerSelectedPosition,
            }
        },
        components: {
            Standards,
            Navbar,
            ActionButton,
            Tooltip,
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
                    return `Resend in ${this.countdown}`;
                }
                else {
                    return 'Send Code';
                }
            },
            isCampaignPeriod() {
                // Check if current datetime is after campaign period
                if (this.isElectionsLoading) {
                    return
                }

                const now = new Date();
                const start = new Date(this.electionsData.CampaignStart);
                const end = new Date(this.electionsData.CampaignEnd);
                
                return now >= start && now < end;
            },
        },
        created() {
            this.intervalId = setInterval(() => {
                let countdownEndTime = localStorage.getItem(`rating_countdown${this.activeElectionIndex}`);
                if (countdownEndTime > 0) {
                    this.countdown--;
                } 
                else {
                    clearInterval(this.intervalId);
                    this.isSent = false;
                }
            }, 1000);
        },
        methods: {
            returnDirectory() {
                router.visit('/directory')
            },
            returnSelection() {
                router.visit('/directory/candidates')
            },
            fileCoc(){
                router.visit('/elections/view/file-coc', {
                    data: {
                        id: this.activeElectionIndex,
                    }
                })
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
                    const countdownDuration = 10; // seconds
                    this.countdown = countdownDuration;

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

                    alert(error.response.data.error)
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
                    if (response.data.valid) {
                        this.isVerified = true;
                        this.rater_student_number = this.student_number;

                        alert('Verification successful.')
                    }
                })
                .catch((error) => {
                    console.log(error)

                    alert('Code does not exist or has used/expired.')
                })
                .finally(() => {
                    this.isVerifying = false;
                })

            },
            submitRating() {
                const ratings = [];

                for (let i = 0; i < this.positionsData.length; i++) {
                    for (let j = 0; j < this.candidatesData.length; j++) {
                        if (this.candidatesData[j].SelectedPositionName === this.positionsData[i].PositionName) {
                            const radio = document.querySelector(`input[name="candidate-rate-${i}-${j}"]:checked`);
                            const ratingValue = radio ? radio.value : '0';

                            const rating = {
                                candidate_student_number: this.candidatesData[j].Student.StudentNumber,
                                rating: ratingValue
                            }

                            ratings.push(rating);
                        }
                    }
                }

                // Check if all ratings are equal to 0
                let allZero = true;
                for (let i = 0; i < ratings.length; i++) {
                    if (ratings[i].rating !== '0') {
                        allZero = false;
                        break;
                    }
                }

                if (allZero) {
                    return alert('Please rate at least one candidate.')
                }

                // Pass the verified student number and rates + student number of candidates to backend
                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/candidates/ratings/submit`, {
                    election_id: this.activeElectionIndex,
                    rater_student_number: this.rater_student_number,
                    ratings: ratings
                })
                .then((response) => {
                    alert('Ratings submitted successfully.')
                    this.closeRateCandidates();
                    this.isVerified = false;
                })
                .catch((error) => {
                    console.log(error)
                    
                    alert(error.response.data.error)
                })
            },
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
        max-height: 70%;
        overflow: auto;
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

    .rate-candidate {
        height: 46px;
        padding: 0 10px;
    }

    .rate-candidate:not(:checked)>input {
        position: absolute;
        top: -9999px;
    }

    .rate-candidate:not(:checked)>label {
        float: right;
        width: 1em;
        overflow: hidden;
        white-space: nowrap;
        font-size: 30px;
        color: #ccc;
    }

    .rate-candidate:not(:checked)>label:before {
        content: '★ ';
    }

    .rate-candidate>input:checked~label {
        color: #EEB503;
    }

    .rate-candidate :not(:checked)>label:hover,
    .rate-candidate :not(:checked)>label:hover~label {
        color: #dfa804;
    }


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

.space{
    margin-left: 10px;
}

.line{
    border: 0;
    height: 2px;
    background: rgb(249,249,249);
    background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgb(176, 176, 176) 50%, rgba(249,249,249,1) 100%);
    margin: 2% 0%;
}

.candidate-list{
    display: flex;
}

.position-sidebar{
    display: flex;
    flex-direction: column;
    width: 20%;
    position: relative;
}

.position-sidebar::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    width: 2px;
    background: linear-gradient(180deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
}

.position-label{
    font-size: 25px;
    font-weight: bold;
}

.select-position{
    text-decoration: none;
    color: black;
    margin: 2% 0%;
}

.select-position:hover{
    color: black;
    font-weight: bold;
}

.active{
    font-weight: bold;
}

.position{
    margin-left: 15%;
    font-size: 20px;
}

.candidate-content{
    margin-left: 2%;
    width: 80%;
}

.candidate{
    background-color: #ffffff;
    box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    border-radius: 6px;
    margin-bottom: 2%;
}

.candidate-wrapper{
    padding: 2%;
    
}

.candidate-information{
    display: flex;
}

.candidate-description{
    margin-left: 2%;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.candidate-img{
    width: 320px;
    height: 440px;
    object-fit: cover;
}

.spacing{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.candidate-name{
    font-weight: bold;
    font-size: 20px;
}

.etc{
    font-size: 20px;
    margin-bottom: 6px;
}

.motto{
    margin-top: 5%;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.platform-label{
    font-size: 20px;
    font-weight: bold;
    margin-top: 5%;
}

.platform{
    font-size: 18px;
}

.rate {
    height: 42px;
}
.rate:not(:checked) > input {
    position:absolute;
    top:-9999px;
}
.rate:not(:checked) > label {
    float:right;
    width:1em;
    overflow:hidden;
    white-space:nowrap;
    cursor:pointer;
    font-size:28px;
    color:#ccc;
}
.rate:not(:checked) > label:before {
    content: '★ ';
}
.rate > input:checked ~ label {
    color: #FFC000;    
}
.rate:not(:checked) > label:hover,
.rate:not(:checked) > label:hover ~ label {
    color: #dfa804;  
}
.rate > input:checked + label:hover,
.rate > input:checked + label:hover ~ label,
.rate > input:checked ~ label:hover,
.rate > input:checked ~ label:hover ~ label,
.rate > label:hover ~ input:checked ~ label {
    color: #F6BB00;
}

.rate-candidate {
    height: 42px;
}
.rate-candidate:not(:checked) > input {
    position:absolute;
    top:-9999px;
}
.rate-candidate:not(:checked) > label {
    width:1em;
    overflow:hidden;
    white-space:nowrap;
    cursor:pointer;
    font-size:28px;
    color:#ccc;
}
.rate-candidate:not(:checked) > label:before {
    content: '★ ';
}
.rate-candidate > input:checked ~ label {
    color: #FFC000;    
}

.rate-candidate > input:checked + label:hover,
.rate-candidate > input:checked + label:hover ~ label,
.rate-candidate > input:checked ~ label:hover,
.rate-candidate > input:checked ~ label:hover ~ label,
.rate-candidate > label:hover ~ input:checked ~ label {
    color: #F6BB00;
}

.candidate-rating{
    background-color: #ffffff;
    box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    border-radius: 6px;
    width: 35%;
}

.candidate-rating-wrapper{
    padding: 3%;
}

.verification-header{
    display: flex;
    align-items: center;
    margin-bottom: 14px;
}

.header-label{
    font-size: 25px;
    font-weight: bold;
    margin: 0;
}

.close-button{
    border: transparent;
    background-color: transparent;
    padding: 0;
    margin-left: auto;
}

.close-svg{
    width: 23px;
    filter: brightness(0) saturate(100%) invert(80%) sepia(0%) saturate(0%) hue-rotate(178deg) brightness(101%) contrast(98%);
}

.question-svg{
    width: 30px;
    margin-left: 10px;
}

.warning{
    font-size: 18px;

}

.code-button{
    width: 100%;
    height: 100%;
    border: transparent;
    border-radius: 6px;
    background-color: #730000;
    color: white;
    align-items: end;
    padding: 0%;
    font-size: 18px;
}

.form-label{
    font-size: 18px;
}

.form-control{
    font-size: 18px;
}

.margin{
    margin-top: 10px;
}

.verify{
    margin-top: 3%;
}

.verify-button{
    width: 100%;
    height: 100%;
    border: transparent;
    border-radius: 6px;
    background-color: #730000;
    color: white;
    align-items: end;
    padding: 1.5%;
    font-size: 18px;
}

.disabled-button:disabled{
    cursor: default;
    background-color: #730000;
    opacity: 0.5;
}

.position-title{
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

.rating{
    display: flex;
    flex-direction: column;
}

.candidate-info{
    font-size: 20px;
}

.top{
    margin-top: 15px;
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

    .return-selection:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .rate-button{
        height: 100%;
        width: 50%;
        border: transparent;
        border-radius: 6px;
        background-color: #730000;
        color: white;
        align-items: end;
        padding: 2%;
        font-size: 18px;
    }

    .rate-button:hover{
        cursor: pointer;
    }

    .rate-button:disabled{
        cursor: default;
        background-color: #730000;
        opacity: 0.5;
    }
</style>