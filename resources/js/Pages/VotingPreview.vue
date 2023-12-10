<template>
    <Navbar></Navbar>
    <title>Voting Preview - Voting System</title>

    <div class="main">
        <h1 class="preview-label">PREVIEW</h1>

        <div class="note">
            <div class="note-content">
                <p>Please note:</p>
            
                <ol>
                    <li><strong>Review Your Choices</strong>: This is your last opportunity to review your choices. 
                        Ensure you have selected the correct candidates or options. Once submitted, changes cannot be made.</li>
                    <li><strong>Understand the Impact</strong>: Your vote is important and can influence the outcome. Be certain that you have made informed decisions.</li>
                    <li><strong>Privacy</strong>: Your vote is confidential. Do not disclose your choices to anyone.</li> 
                    <li><strong>Final Submission</strong>: Once you click the submit button, your choices will be final. There is no option to retract or modify them.</li> 
                </ol>

                <p style="margin: 0%;">Remember, every vote counts. Make yours count too! Proceed with caution.</p>
            </div>
        </div>

        <div v-for="(candidates, position) in votes" class="selected-candidates">
            <div class="candidate">
                <h1 class="position">{{ position }}</h1>

                <div class="candidate-information-wrapper">
                    <div v-for="vote in candidates" class="candidate-information">
                        <img v-if="vote === 'abstain'" src="../../images/abstain.svg" class="candidate-photo" draggable="false">
                        <img v-else :src="vote.DisplayPhoto" alt="" class="candidate-photo" draggable="false">
                        <h1 class="candidate-name">{{ vote === 'abstain' ? 'Abstain' : vote.Student.FirstName + ' ' + vote.Student.LastName }}</h1>
                        <h2 class="candidate-affiliation">{{ vote === 'abstain' ? '' : (vote.PartyListId ? vote.PartyListName : 'Independent') }}</h2>
                    </div>
                </div>
            </div>
        </div>

        <div class="preview-buttons">
            <button class="back-button" @click.prevent="returnPage">RETURN</button>
            <button class="submit-button" @click.prevent="confirm">CONFIRM</button>
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
    
    export default {
        setup(props) {
            const activeElectionIndex = ref(Number(props.id));
            const votes = ref(props.votes);
            const student_number = ref(props.student_number);
            const confirm_clicked = ref(false);
            
            return {
                activeElectionIndex,
                votes,
                student_number,
                confirm_clicked
            };
        },
        components: { Navbar },
        props: {
            id: '',
            votes: {},
            student_number: '',
        },
        methods: {
            returnPage(){
                router.visit(`/voting/process?id=${this.activeElectionIndex}`);
            },
            confirm(){
                this.confirm_clicked = true;
                const votesList = {
                    election_id: this.activeElectionIndex,
                    voter_student_number: this.student_number,
                    votes: Object.values(this.votes).flat().map(candidate => {
                        return { 
                            candidate_student_number: candidate === 'abstain' ? 'abstain' : candidate.StudentNumber 
                        };
                    }),
                };

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/votings/submit`, votesList)
                    .then(response => {
                        console.log(response.data);
                        localStorage.removeItem(`votes-${this.activeElectionIndex}`);

                        alert('Your votes has been submitted, you will be logged out now.');

                        this.logout();
                    })
                    .catch(error => {
                        console.error(error);
                        this.confirm_clicked = false;
                        
                        alert(error.response.data.error)
                    });
            },
            logout(){
                // Clear the local storage anything name starts from votes
                for (const [key, value] of Object.entries(localStorage)) {
                    if (key.startsWith('votes')) {
                        localStorage.removeItem(key);
                    }
                }

                axios.post('/logout')
                    .then(response => {
                        useUserStore().reset(); // Reset the user store 
                        location.reload(); // trick the system to logout and prevent backing 
                                         // (Reloading to check for cookie token and throw back to login page)

                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        },
    };
</script>

<style scoped>
   .main{
        margin: 1.5% 8%;
    }

    .preview-label{
        font-weight: 700;
        font-size: 30px;
        color: #800000;
        margin: 0;
        margin: 1.5% 0%;
    }

    .note{
        background-color: white;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .note-content{
        padding: 1.5%;
    }

    .selected-candidates{
        background-color: white;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        margin: 1.5% 0%;
        text-align: center;
        display: flex;
        justify-content: center;
    }

    .candidate{
        padding: 1.5%;
        width: 100%;
        text-align: center;
    }

    .position{
        font-weight: 700;
        font-size: 27px;
        margin: 0%;
    }

    .candidate-information-wrapper{
        display: flex;
        justify-content: center;
        margin: 0%;
        width: 100%;
        flex-wrap: wrap;
    }

    .candidate-information{
        width: 300px;
        height: 300px;
        padding: 2%;
        background-color: white;
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 1.5% 1%;
        transition: all 0.4s ease;
    }

    .candidate-photo{
        width: 170px;
        height: 170px;
        border-radius: 50%;
        object-fit: cover;
    }

    .candidate-information:hover {
        background-color: rgb(239, 239, 239);
        box-shadow: 0px 3.5px 5px rgba(167, 165, 165, 0.7);
    }

    .candidate-name{
        font-size: 20px;
        margin: 8% 0%;
        font-weight: bold;
    }

    .candidate-affiliation{
        margin-top: -5%;
        font-size: 17px;
    }

    .preview-buttons{
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        padding: 1.5% 0%;
        display: flex;
        justify-content: space-between;
    }

    .back-button{
        border: transparent;
        margin: 0% 1.5%;
        color: #800000;
        background-color: transparent;
        font-weight: 900;
        font-size: 23px;
        padding: 8px 32px;
    }

    .submit-button{
        border: transparent;
        margin: 0% 1.5%;
        color: white;
        background-color: #800000;
        font-weight: 900;
        font-size: 23px;
        padding: 8px 32px;
        border-radius: 6px;
    }
    
</style>