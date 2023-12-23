<template>
    <title>Directory Election Winners - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h2 class="my-1 page-title">
                <span class="return" @click="returnPage">Directory</span> > Election Winners
            </h2>
        </div>

        <a href="" class="select-election">
            <div class="election">
                <div class="election-content">
                    <img src="ssc.png" alt="" class="organization-logo">
                    <h1 class="election-title">GRAND SSC ELECTION S.Y. 2023</h1>
                </div>
            </div>
        </a>

        <a href="" class="select-election">
            <div class="election">
                <div class="election-content">
                    <img src="commits.png" alt="" class="organization-logo">
                    <h1 class="election-title">COMMITS ELECTION</h1>
                </div>
            </div>
        </a>
    </div>
</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watch, watchEffect } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import ImageSkeleton from '../../Skeletons/ImageSkeleton.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup() {
           

            return {
                
            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            BaseContainer,
            BaseTable,
            ImageSkeleton,
        },
        methods: {
            returnPage() {
                router.visit('/comelec/directory');
            }
        }
    }
</script>

<style scoped>
   .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Inter', sans-serif;
        margin-right: 3%;
    }

    .header{
        display: flex;
        align-items: center;
        margin: 0% -1%;
        justify-content: space-between;
    }

    .return{
        color: #B90321;
        cursor: pointer;
    }

    .return:hover{
        text-decoration: underline;
    }

    .page-title{
        font-weight: 900;
        font-size: 28px;
        margin: 0%;
    }

    .election{
        margin: 1.5% -1%;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
    }

    .election-content{
        padding: 1%;
        display: flex;
        align-items: center;
    }

    .select-election{
        color: black;
        text-decoration: none;
    }

    .organization-logo{
        width: 70px;
        height: 70px;
    }

    .election-title{
        margin: 0% 0% 0% 1.5%;
        width: 100%;
        font-weight: 600;
        font-size: 25px;
    }

    .election:hover{
        color: #800000;
        background-color: #f4f4f4;
    }   
</style>