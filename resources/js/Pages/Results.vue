<template>
    <title>Results - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="main">
        <h1 class="election-name">GRAND SSC ELECTION SY 2023 RESULTS</h1>

        <div class="candidates-votes">
            <div class="dropdown">
                <h6 class="position dropdown-toggle">PRESIDENT</h6>
            </div>
            <div class="candidate1">
                <div class="candidate-information">
                    <span class="rank">1st</span>
                    <img src="../../images/dog_placeholder.jpg" alt="" class="candidate-photo">
                    <span class="candidate-name">David Daniel Reataza</span>

                    <div class="vote-count">
                        <span>25 votes</span>
                        <span>26.32%</span>
                    </div>
                </div>
            </div>

            <div class="candidate2">
                <div class="candidate-information">
                    <span class="rank">2nd</span>
                    <img src="../../images/dog_placeholder.jpg"  alt="" class="candidate-photo">
                    <span class="candidate-name">Roselyn Viray</span>

                    <div class="vote-count">
                        <span>20 votes</span>
                        <span>21.05%</span>
                    </div>
                </div>
            </div>

            <div class="candidate3">
                <div class="candidate-information">
                    <span class="rank">3rd</span>
                    <img src="../../images/dog_placeholder.jpg"  alt="" class="candidate-photo">
                    <span class="candidate-name">Random Student</span>

                    <div class="vote-count">
                        <span>18 votes</span>
                        <span>18.95%</span>
                    </div>
                </div>
            </div>

            <div class="candidate">
                <div class="candidate-information">
                    <span class="rank">4th</span>
                    <img src="../../images/dog_placeholder.jpg"  alt="" class="candidate-photo">
                    <span class="candidate-name">Random Student A</span>

                    <div class="vote-count">
                        <span>17 votes</span>
                        <span>17.89%</span>
                    </div>
                </div>
            </div>

            <div class="candidate">
                <div class="candidate-information">
                    <span class="rank">5th</span>
                    <img src="../../images/dog_placeholder.jpg"  alt="" class="candidate-photo">
                    <span class="candidate-name">Random Student B</span>

                    <div class="vote-count">
                        <span>15 votes</span>
                        <span>15.79%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed } from 'vue';
    import axios from 'axios';

    export default {
        setup() {

        },
        components: {
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
            ImageSkeleton
        }
    }
</script>

<style scoped>
    .main{
        margin: 2% 5%;
        font-family: 'Inter', sans-serif;
    }

    .election-name{
        font-weight: 700;
        font-size: 30px;
        color: #800000;
        margin: 0;
    }

    .candidates-votes{
        padding-bottom: 0.5%;
        margin: 1.5% 0%;
        background-color: white;
        border-radius: 6px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .position{
        font-weight: 900;
        font-size: 27px;
        margin: 0%;
    }

    .dropdown{
        padding: 1.5% 2% 0% 2%;
    }

    .candidate{
        margin: 1.5% 2%;
        background-color: white;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate1{
        background: rgb(255,235,131);
        background: linear-gradient(90deg, rgba(255,235,131,1) 0%, rgba(255,214,83,1) 50%, rgba(255,230,139,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate2{
        background: rgb(237,237,237);
        background: linear-gradient(90deg, rgba(237,237,237,1) 0%, rgba(208,206,206,1) 50%, rgba(242,242,242,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate3{
        background: rgb(239,194,113);
        background: linear-gradient(90deg, rgba(239,194,113,1) 0%, rgba(188,128,8,1) 50%, rgba(250,219,156,1) 100%);
        margin: 1.5% 2%;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .candidate-information{
        display: flex;
        align-items: center;
        position: relative;
        padding: 0.5% 2%;
    }

    .rank{
        font-size: 30px;
        font-weight: 900;
        margin: 0%;
        padding: 0%;
        width: 70px;
        text-align: center;
    }

    .candidate-photo{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0% 1.5%;
    }

    .candidate-name{
        font-size: 20px;
        font-weight: bold;
    }

    .vote-count{
        display: flex;
        flex-direction: column;
        text-align: end;
        position: absolute;
        right: 2%;
        font-weight: bold;
        font-size: 18px;
    }
</style>