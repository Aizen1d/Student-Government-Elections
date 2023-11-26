<template>
    <Navbar></Navbar>
    <div class="main">
        <h1 class="header-label">ELECTIONS</h1>

        <a href="" class="select-election">
            <div class="election">
                <div class="election-content">
                    <img src="../../images/ssc.png" alt="" class="organization-logo">
                    <h1 class="election-title">GRAND SSC ELECTION S.Y. 2023</h1>
                </div>
            </div>
        </a>

        <a href="" class="select-election">
            <div class="election">
                <div class="election-content">
                    <img src="../../images/commits.png" alt="" class="organization-logo">
                    <h1 class="election-title">COMMITS ELECTION</h1>
                </div>
            </div>
        </a>
    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';
    import { useUserStore } from '../Stores/UserStore.js';

    export default {
        setup(props) {
            const userStore = useUserStore();

            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            
            return {

            };
        },
        components: { Navbar },
        props: {
            student_number: '',
            full_name: '',
        },
    };
</script>

<style scoped>
    .main{
        margin: 1.5% 8%
    }

    .header-label{
        font-weight: 700;
        font-size: 30px;
        color: #800000;
        margin: 0;
    }

    .select-election{
        text-decoration: none;
        color: black;
    }

    .election {
        margin: 1.5% 0%;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .election::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgb(211, 211, 211);
        transition: all 600ms ease-out;
    }

    .election:hover::before {
        left: 0;
    }

    .election-content {
        padding: 1.5%;
        display: flex;
        align-items: center;
        position: relative;
    }

    .organization-logo{
        width: 70px;
        height: 70px;
    }

    .election-title{
        margin: 0% 0% 0% 3%;
        width: 100%;
        font-weight: 700;
        font-size: 30px;
    }
    
</style>