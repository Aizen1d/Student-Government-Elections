<template>
    <title>Voting Process - Voting System</title>
    <Navbar></Navbar>

    <div style="text-align: center;" v-if="isCandidatesPerPositionLoading">
        <h1 style="margin-top: 2%;">
            Preparing data for voting process...
        </h1>
    </div>

    <div class="election-header">
        <h1 class="election-title" v-if="!isCandidatesPerPositionLoading">{{ electionsData.ElectionName }}</h1>
    </div>

    <template v-if="atLeastOneCandidate && !isCandidatesPerPositionLoading" 
            v-for="(candidates, positionName, candidateIndex) in candidatesPerPositionData" :key="candidateIndex">
        <div class="position">
            <div class="position-information">
                <h2 class="position-label">{{ positionName }}</h2>
                <p class="position-instructions">
                    Please select {{ candidates[candidateIndex].PositionQuantity > 1 ? 'maximum of' : '' }} ({{ candidates[candidateIndex].PositionQuantity }}) candidate or choose to abstain.
                </p>
            </div>

            <div class="position-candidates">
                <div v-for="(candidate, index) in candidates" :key="index" class="candidate" :class="{ 'voted': isVoted(candidate, positionName) }" @click="vote(candidate, positionName)">
                    <div class="candidate-card">
                        <img :src="candidate.DisplayPhoto" class="candidate-photo" alt="" draggable="false">
                        <h3 class="candidate-name">{{ candidate.Student.FirstName + " " + (candidate.Student.MiddleName ? candidate.Student.MiddleName + " " : "") + candidate.Student.LastName }}</h3>
                        <h4 class="candidate-affiliation" v-if="candidate.PartyListName">{{ candidate.PartyListName }}</h4>
                        <h4 class="candidate-affiliation" v-else>Independent</h4>
                    </div>
                </div>
                <div class="candidate" :class="{ 'voted': isAbstain(positionName) }" @click="abstain(positionName)">
                    <div class="candidate-card">
                        <img src="../../images/abstain.svg" class="candidate-photo" alt="" draggable="false">
                        <h3 class="candidate-name">Abstain</h3>
                    </div>
                </div>
            </div>
        </div>
    </template>

    <div v-if="!atLeastOneCandidate && !isCandidatesPerPositionLoading" style="text-align: center;">
        <h1 style="font-family: 'Inter', sans-serif;">
            (No candidates in this election)
        </h1>
    </div>

    <div v-if="!isCandidatesPerPositionLoading" class="election-buttons">
        <button class="back-button" @click.prevent="goBack">RETURN</button>
        <button v-if="atLeastOneCandidate" class="submit-button" @click.prevent="submitVotes">SUBMIT</button>
    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';
    import Body from '../Shared/Body.vue';

    import { ref } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'
    import { useLocalStorage } from '@vueuse/core';

    export default {
        setup(props) {
            const activeElectionIndex = ref(Number(props.id));
            const atLeastOneCandidate = ref(useLocalStorage(`atLeastOneCandidate-${activeElectionIndex.value}`, false));
            const votes = ref(useLocalStorage(`votes-${activeElectionIndex.value}`, {}));

            // For checking if voting period is still ongoing?
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
            
                const fetchCandidatsPerSelectedPosition = async () => {
                    return axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/candidates/election/per-position/${activeElectionIndex.value}/all`)
                        .then(response => {
                        console.log(`Get all candidates from selected election successful. Duration: ${response.duration}ms`);

                        let hasCandidates = false;
                        for (let position in response.data.candidates) {
                            if (response.data.candidates[position].length > 0) {
                            hasCandidates = true;
                            break;
                            }
                        }

                        if (hasCandidates) {
                            atLeastOneCandidate.value = true;
                        } else {
                            atLeastOneCandidate.value = false;
                        }

                        return response.data.candidates;
                    })
                    .catch(error => {
                    console.log(error);
                    });
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
                atLeastOneCandidate,
                electionsData,
                votes,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,

                positionsData,
                isPositionsLoading,
                isPositionsSuccess,
                isPositionsError,
                isPositionsRefetching,
                positionsRefetch,

                candidatesPerPositionData,
                isCandidatesPerPositionLoading,
                isCandidatesPerPositionSuccess,
                isCandidatesPerPositionError,
                isCandidatesPerPositionRefetching,
            };
            
        },
        components: { Navbar },
        props: {
            id: '',
        },
        mounted() {
           
        },
        methods: {
            goBack() {
                router.visit('/home');
            },
            vote(candidate, positionName) {
                // Check if this position already has votes
                if (!this.votes[positionName]) {
                    this.votes[positionName] = [];
                }

                // Check if the user has already voted for this candidate
                const candidateIndex = this.votes[positionName].map(votedCandidate => votedCandidate.StudentNumber).indexOf(candidate.StudentNumber);

                if (candidateIndex > -1) {
                    // If the user has already voted for this candidate, remove the vote
                    this.votes[positionName].splice(candidateIndex, 1);
                    console.log('You removed your vote for', candidate.Student.FirstName, 'for the position of', positionName);
                }
                else {
                    // Check if the user has abstained for this position
                    if (this.isAbstain(positionName)) {
                        this.votes[positionName] = [];
                    }

                    // Check if the maximum number of votes for this position has been reached
                    if (this.votes[positionName].length < this.candidatesPerPositionData[positionName][0].PositionQuantity) {
                        this.votes[positionName].push(candidate);
                        console.log('You voted for', candidate.Student.FirstName, 'for the position of', positionName);
                    } 
                    else {
                    // If the maximum number of votes has been reached, replace the first vote with the new vote
                        this.votes[positionName].shift();
                        this.votes[positionName].push(candidate);
                        console.log('You changed your vote to', candidate.Student.FirstName, 'for the position of', positionName);
                    }
                }
            },
            abstain(positionName) {
                // Check if the user has already abstained for this position
                if (this.isAbstain(positionName)) {
                    // If the user has already abstained, remove the abstention
                    this.votes[positionName] = [];
                    console.log('You removed your abstention for', positionName);
                } else {
                    // If the user hasn't abstained, add the abstention
                    this.votes[positionName] = ['abstain'];
                    console.log('You abstained from voting for', positionName);
                }
            },
            isVoted(candidate, positionName) {
                return this.votes[positionName] && this.votes[positionName].map(votedCandidate => votedCandidate.StudentNumber).includes(candidate.StudentNumber);
            },
            isAbstain(positionName) {
                return this.votes[positionName] && this.votes[positionName].includes('abstain');
            },
            hasVotedOrAbstained(positionName) {
                return this.votes[positionName] && this.votes[positionName].length > 0;
            },
            validateVotes() {
                for (let positionName in this.candidatesPerPositionData) {
                    if (!this.hasVotedOrAbstained(positionName)) {
                        alert('You must vote for at least one candidate or abstain in the position of ' + positionName);
                        return false;
                    }
                }

                /* print each name of the candidate and position and is not abstain
                for (let position in this.votes) {
                    if (this.votes[position].length > 0) {
                        for (let candidate in this.votes[position]) {
                            if (this.votes[position][candidate] != 'abstain') {
                                console.log(this.votes[position][candidate].Student.FirstName + ' ' + position);
                            }
                        }
                    }
                }*/

                return true;
            },
            submitVotes() {
                if (this.validateVotes()) {
                    
                    router.post('/voting/preview', {
                        id: String(this.activeElectionIndex),
                        votes: this.votes,
                    });
                }
            }
        }
    };

</script>

<style scoped>
    .main{
        font-family: 'Inter', sans-serif;
    }

    .election-header{
        background-color: white;
        margin: 2% 4%;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .election-title{
        margin: 0%;
        font-family: 'Inter', sans-serif;
        text-align: center;
        padding: 1.5% 0%;
        font-size: 38px;
        font-weight: 800;
    }

    .position{
        background-color: white;
        margin: 2% 4%;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        padding-bottom: 3%;
        border-radius: 6px;
    }

    .position-information{
        padding: 4% 3% 1% 3%;
    }

    .position-label{
        font-weight: 900;
        font-size: 30px;
        margin-bottom: 1%;
        text-transform: uppercase;
    }

    .position-instructions{
        font-size: 18px;
    }

    .position-candidates{
        margin: 0% 3%;
        display: flex; 
        flex-wrap: wrap; 
    }

    .candidate{
        width: 330px;
        height: 330px;
        padding: 2%;
        text-align: center;
        background-color: white;
        margin: 1% 1%;
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: transform 0.4s ease;
    }

    .candidate:hover {
        cursor: pointer;
        transform: translateY(-12px);
        background-color: rgb(245, 245, 245);
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.7);

        .candidate-photo{
            filter: grayscale(0%);
        }
    }

    .voted{
        border: 5px solid #4eb358;
        
        .candidate-photo{
            filter: grayscale(0%);
        }
    }

    .candidate-photo{
        cursor: pointer;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        object-fit: cover;
        filter: grayscale(100%);
        transition: filter 0.3s ease;
    }

    .candidate-name{
        font-size: 20px;
        margin: 15% 0%;
        font-weight: bold;
    }

    .candidate-affiliation{
        margin-top: -10%;
        font-size: 17px;
    }

    input[type="radio"] {
        position: absolute;
        opacity: 0;
        width: 330px;
        height: 330px;
    }

    input[type="radio"]:checked + label {
        .candidate-photo{
            filter: grayscale(0%);
        }
    }

    .election-buttons{
        background-color: white;
        margin: 2% 4%;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        padding: 1.5% 0%;
        display: flex;
        justify-content: space-between;
    }

    .back-button{
        border: transparent;
        margin: 0% 1.5%;
        color: #FFC000;
        background-color: transparent;
        font-weight: 900;
        font-size: 23px;
        padding: 8px 32px;
    }

    .submit-button{
        border: transparent;
        margin: 0% 1.5%;
        color: white;
        background-color: #FFD966;
        font-weight: 900;
        font-size: 23px;
        padding: 8px 32px;
        border-radius: 6px;
    }
</style>
