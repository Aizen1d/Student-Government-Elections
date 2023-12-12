<template>
    <title>Directory - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="header row">
        <div class="col">
            <h1 class="eligible">
                
            </h1>
        </div>
    </div>

    <div class="main">
        <div class="card-deck">
            <div class="card" @click.prevent="viewVoters">
                <img src="../../images/Directory/List/voter.png" class="card-img-top" alt="">
                <div class="card-body">
                    <h1 class="card-title">Eligible Voters</h1>
                </div>
            </div>

            <div class="card" @click.prevent="viewCandidates">
                <img src="../../images/Directory/List/candidate.png" class="card-img-top" alt="">
                <div class="card-body">
                    <h1 class="card-title">Candidates</h1>
                </div>
            </div>

            <div class="card" @click.prevent="viewPartylists">
                <img src="../../images/Directory/List/party.png" class="card-img-top" alt="">
                <div class="card-body">
                    <h1 class="card-title">Party Lists</h1>
                </div>
            </div>

            <div class="card">
                <img src="../../images/Directory/List/orgs.png" class="card-img-top" alt="">
                <div class="card-body">
                    <h1 class="card-title">Student Organizations</h1>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'

    import { router } from '@inertiajs/vue3'

    export default {
        setup() {
            return {
                
            }
        },
        components: {
            Standards,
            Navbar
        },
        methods: {
            viewVoters(){
                router.visit('/directory/voters')
            },
            viewCandidates(){
                router.visit('/directory/candidates')
            },
            viewPartylists(){
                router.visit('/directory/partylists')
            },
        }
    }
</script>

<style scoped>
    .eligible{
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .header{
        margin-top: 1.8%;
        margin-left: 2.5%;
        width: 78%;
    }
    .main{
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .card-deck{
        display: flex;
    }

    .card {
        width: 24rem;
        height: 40rem;
        border-radius: 0px;
        overflow: hidden;
        cursor: pointer;
        position: relative;
        margin: 3% 0.5%;
        background-color: #880000;
    }

    .card img {
        position: absolute;
        object-fit: cover;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        opacity: 0.18;
    }

    .card:hover, .card img:hover{
        background-color: transparent;
        opacity: 1;
        transition: .5s ease-out;
    }

    .card img:hover{
        transform: scale(1.01);
    }

    .card-body{
        color: white;
        opacity: 1;
        text-align: center;
        margin-top: 140%;
        background-color: #4f0b0b;
    }

    .card-body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .card-title {
        margin: auto;
    }

    .card-title{
        font-size: 35px;
    }
</style>