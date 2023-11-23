<template>
    <form class="main">
        <div class="election-header">
            <h1 class="election-title">GRAND SSC ELECTION S.Y. 2023</h1>
        </div>
        <div class="position">
            <div class="position-information">
                <h2 class="position-label">PRESIDENT</h2>
                <p class="position-instructions">Please select one (1) candidate or choose to abstain.</p>
            </div>
            <div class="position-candidates">
                <div class="candidate">
                    <input type="radio" id="candidate1" name="president">
                    <label for="candidate1">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="candidate2" name="president">
                    <label for="candidate2">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="candidate3" name="president">
                    <label for="candidate3">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="candidate4" name="president">
                    <label for="candidate4">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="abstain1" name="president">
                    <label for="abstain1">
                        <img src="../../images/abstain.svg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">Abstain</h3>
                    </label>
                </div>
            </div>
        </div>
        <div class="position">
            <div class="position-information">
                <h2 class="position-label">VICE PRESIDENT</h2>
                <p class="position-instructions">Please select one (1) candidate or choose to abstain.</p>
            </div>
            <div class="position-candidates">
                <div class="candidate">
                    <input type="radio" id="vice-president1" name="vice-president">
                    <label for="vice-president1">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="vice-president2" name="vice-president">
                    <label for="vice-president2">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="vice-president3" name="vice-president">
                    <label for="vice-president3">
                        <img src="../../images/candidate.jpg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">David Daniel Reataza</h3>
                        <h4 class="candidate-affiliation">Independent</h4>
                    </label>
                </div>
                <div class="candidate">
                    <input type="radio" id="abstain2" name="vice-president">
                    <label for="abstain2">
                        <img src="../../images/abstain.svg" class="candidate-photo" alt="">
                        <h3 class="candidate-name">Abstain</h3>
                    </label>
                </div>
            </div>
        </div>

        <div class="election-buttons">
            <button class="back-button">GO BACK</button>
            <button class="submit-button">SUBMIT</button>
        </div>
    </form>

    <title>Voting Process - Voting System</title>
</template>

<script>
    import axios from 'axios';
    import Body from '../Shared/Body.vue';

    export default {
        setup() {

        },
        components: { Body },
       
        methods: {
             
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
        text-align: center;
        padding: 1.5% 0%;
        font-size: 35px;
        font-weight: 900;
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
        transition: transform 0.4s ease;
    }

    .candidate:hover {
        transform: translateY(-10px);
        
        .candidate-photo{
            filter: grayscale(0%);
        }
    }

    .candidate-photo{
        width: 170px;
        height: 170px;
        border-radius: 50%;
        object-fit: cover;
        filter: grayscale(100%);
        transition: filter 0.3s ease;
    }

    .candidate-name{
        font-size: 18px;
        margin: 7% 0%;
        font-weight: bold;
    }

    .candidate-affiliation{
        font-size: 18px;
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
