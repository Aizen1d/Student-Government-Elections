<template>
    <title>Directory Candidates - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="scroll-up">
        <a @click="topFunction" id="mybutton">
            <img src="../../images/Directory/Candidates/scroll-up.svg" alt="" width="60px">
        </a>
    </div>

    <div class="sidebar">
        <div class="choices">
            <h1>CANDIDATES</h1>
            <div class="options">
                <a href="#pos1">President</a>
                <a href="#pos2">Vice President</a>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="position row">
            <h1 id="pos1" class="col-10">President Candidates</h1>
            <button class="col-2 rate-button">Rate Candidates ★</button>

            <hr class="my-4">
            
            <div class="candidate">
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <img src="../../images/dog_placeholder.jpg" class="cpic" alt="">
                            </td>
                            <td class="info">
                                <div class="data">
                                    <div class="align">
                                        <div class="name">
                                            <strong>David Daniel D. Reataza</strong>
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
                                   
                                <div class="affiliation">Independent</div>
                                </div>
                                
                                
                                <div class="quote">
                                    <em>"Believe you can and you're halfway there."</em>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <hr class="my-4">

            <div class="candidate">
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <img src="../../images/dog_placeholder.jpg" class="cpic" alt="">
                            </td>
                            <td class="info">
                                <div class="data">
                                    <div class="align">
                                        <div class="name">
                                            <strong>David Daniel D. Reataza</strong>
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
                                   
                                <div class="affiliation">Independent</div>
                                </div>
                                
                                <div class="quote">
                                    <em>"Success is not final, failure is not fatal: It is the courage to continue that counts."</em>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="position">
            <h1 id="pos2">Vice President Candidates</h1>

            <hr class="my-4">
            
            <div class="candidate">
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <img src="../../images/dog_placeholder.jpg" class="cpic" alt="">
                            </td>
                            <td class="info">
                                <div class="data">
                                    <strong>David Daniel D. Reataza <br></strong>
                                Independent
                                </div>
                                
                                <div class="quote">
                                    <em>"Believe you can and you're halfway there."</em>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <hr class="my-4">

            <div class="candidate">
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <img src="../../images/dog_placeholder.jpg" class="cpic" alt="">
                            </td>
                            <td class="info">
                                <div class="data">
                                    <strong>David Daniel D. Reataza <br></strong>
                                Independent
                                </div>
                                
                                <div class="quote">
                                    <em>"Success is not final, failure is not fatal: It is the courage to continue that counts."</em>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'

    import { ref, onMounted, onUnmounted } from 'vue';

    export default {
        setup() {
            /*const mybutton = ref(null);

            const topFunction = () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

            onMounted(() => {
                const scrollFunction = () => {
                    if (window.scrollY > 20) {
                        mybutton.style.display = "block";
                    } else {
                        mybutton.style.display = "none";
                    }
                }

                window.addEventListener('scroll', scrollFunction);
            });

            onUnmounted(() => {
                window.removeEventListener('scroll', scrollFunction);
            });

            return { mybutton, topFunction };*/
        },
        components: {
            Standards,
            Navbar
        },
        methods: {
         
        }
    }
</script>

<style scoped>
    .sidebar{
        height: 100%; /* Full-height: remove this if you want "auto" height */
        width: 300px; /* Set the width of the sidebar */
        position: fixed; /* Fixed Sidebar (stay in place on scroll) */
        top: 1;
        left: 0;
        overflow-x: hidden; /* Disable horizontal scroll */
        padding-top: 1.5%;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .choices{
        text-align: start;
        margin: 0% 10%;
    }

    .choices h1{
        color: #9A000A;
        font-size: 30px;
        font-weight: 900;
    }

    .options{
        margin: 0%;
        margin-top: 10%;
        display: grid;
    }

    .options a{
        margin: 3% 0%;
        text-decoration: none;
        color: black;
        font-size: 18px;
    }

    .main{
        margin-left: 300px;
        font-family: 'Source Sans Pro', sans-serif;
        margin-top: 5%;
    }

    .position{
        margin: 5% 2%;
    }

    .position h1{
        color: #9A000A;
        font-size: 29px;   
        font-weight: 700;
        margin: 0%;
    }

    .rate-button{
        border: transparent;
        background-color: #880000;
        color: white;
        border-radius: 3px;
        padding: 1% 0%;
    }

    .candidate{
        width: 100%;
    }

    .cpic{
        width: 320px;
        height: 440px;
        object-fit: cover;
    }

    .info{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 22px;
        width: 100%;
        padding: 0% 2%;
    }

    .align{
        display: flex;
        align-items: center;
    }

    .quote{
        text-align: center;
        margin-top: 50px;
    }

    .candidate:hover{
        color: #CA2B00;
    }

    .candidate td {
        vertical-align: top;
    }

    .scroll-up{
        display: block;
        position: fixed; /* Fixed/sticky position */
        bottom: 100px; /* Place the button at the bottom of the page */
        right: 110px; /* Place the button 30px from the right */
        z-index: 99; /* Make sure it does not overlap */
        filter: invert(12%) sepia(37%) saturate(6821%) hue-rotate(344deg) brightness(105%) contrast(119%);
    }

    .scroll-up:hover{
        filter: invert(86%) sepia(41%) saturate(799%) hue-rotate(354deg) brightness(93%) contrast(97%);
    }

    .rate {
        height: 46px;
        padding: 0 10px;
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
        font-size:30px;
        color:#ccc;
    }
    .rate:not(:checked) > label:before {
        content: '★ ';
    }
    .rate > input:checked ~ label {
        color: #EEB503;    
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
        color: #c59b08;
    }
</style>