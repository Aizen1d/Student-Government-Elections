<template>
    <Navbar></Navbar>
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

        <div class="selected-candidates">
            <div class="candidate">
                <h1 class="position">PRESIDENT</h1>

                <div class="candidate-information-wrapper">
                    <div class="candidate-information">
                        <img src="../../images/candidate.jpg" alt="" class="candidate-photo">
                        <h1 class="candidate-name">David Daniel Reataza</h1>
                        <h2 class="candidate-affiliation">Independent</h2>
                    </div>
                </div>
            </div>
        </div>

        <div class="selected-candidates">
            <div class="candidate">
                <h1 class="position">VICE PRESIDENT</h1>

                <div class="candidate-information-wrapper">
                    <div class="candidate-information">
                        <img src="../../images/candidate.jpg" alt="" class="candidate-photo">
                        <h1 class="candidate-name">Roselyn Viray</h1>
                        <h2 class="candidate-affiliation">Enigma</h2>
                    </div>
                    <div class="candidate-information">
                        <img src="../../images/candidate.jpg" alt="" class="candidate-photo">
                        <h1 class="candidate-name">Roselyn Viray</h1>
                        <h2 class="candidate-affiliation">Enigma</h2>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="preview-buttons">
            <button class="back-button">GO BACK</button>
            <button class="submit-button">SUBMIT</button>
        </div>
    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';

    export default {
        setup() {
            
        },
        components: { Navbar },
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
    }

    .candidate-photo{
        width: 170px;
        height: 170px;
        border-radius: 50%;
        object-fit: cover;
    }

    .candidate-name{
        font-size: 18px;
        margin: 3% 0%;
        font-weight: bold;
    }

    .candidate-affiliation{
        font-size: 18px;
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