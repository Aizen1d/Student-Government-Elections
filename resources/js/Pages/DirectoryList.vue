<template>
    <title>Directory - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="header">DIRECTORY</h1>

        <div class="directory-list">
            <div @click.prevent="viewVoters" class="select">
                <div class="card">
                    <img src="../../images/Directory/List/voter.png" class="card-img-top" alt="">
                    <div class="card-body">
                        <h1 class="card-title">Eligible Voters</h1>    
                    </div>
                </div>
            </div>
            
            <div @click.prevent="viewCandidates" class="select">
                <div class="card">
                    <img src="../../images/Directory/List/candidate.png" class="card-img-top" alt="">
                    <div class="card-body">
                        <h1 class="card-title">Candidates</h1>
                    </div>
                </div>
            </div>
            
            <div @click.prevent="viewPartylists" class="select">
                <div class="card">
                    <img src="../../images/Directory/List/party.png" class="card-img-top" alt="">
                    <div class="card-body">
                        <h1 class="card-title">Party Lists</h1>
                    </div>
                </div>
            </div>

            <div @click.prevent="viewStudentOrganizations" class="select">
                <div class="card">
                    <img src="../../images/Directory/List/orgs.png" class="card-img-top" alt="">
                    <div class="card-body">
                        <h1 class="card-title">Student Organizations</h1>
                    </div>
                </div>
            </div>
        </div>
    </main>
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
            viewStudentOrganizations(){
                router.visit('/directory/student-organization')
            }
        }
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
    }

    .directory-list{
        display: flex;
        justify-content: space-between;
    }

    .card {
        width: 26.5rem;
        height: 44rem;
        border-radius: 0px;
        overflow: hidden;
        cursor: pointer;
        position: relative;
        background-color: #630303;
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
        z-index: 1;
        text-align: center;
        margin-top: 140%;
        background-color: rgba(78, 3, 3, 0.77);
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
        font-size: 30px;
    }

    .select{
        text-decoration: none;
    }

    .card:hover .card-body, .card-body:hover {
        display: none;
    }

    .card:hover {
        background-color: white;
    }
</style>