<template>
    <title>Directory - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h1 class="page-title">Directory</h1>
        </div>
        <div @click="" class="select-directory">
            <div class="directory">
                <div class="directory-content">
                    <img src="../../../images/icons/winner.svg" alt="" class="logo">
                    <h1 class="directory-title">ELECTION WINNERS</h1>
                </div>
            </div>
        </div>

        <div @click="" class="select-directory">
            <div class="directory">
                <div class="directory-content">
                    <img src="../../../images/icons/organization.svg" alt="" class="logo">
                    <h1 class="directory-title">STUDENT ORGANIZATIONS</h1>
                </div>
            </div>
        </div>

        <div @click="certifications" class="select-directory">
            <div class="directory">
                <div class="directory-content">
                    <img src="../../../images/icons/certification.svg" alt="" class="logo">
                    <h1 class="directory-title">CERTIFICATIONS</h1>
                </div>
            </div>
        </div>
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
            electionWinners(){
                router.visit('/comelec/directory/election-winners');
            },
            studentOrganizations(){
                router.visit('/comelec/directory/student-organizations');
            },
            certifications(){
                router.visit('/comelec/directory/certifications');
            }
        }
    }
</script>

<style scoped>
    /*!!!START OF CSS!!!*/

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

    .page-title{
        font-weight: 800;
        margin: 0%;
        margin-left: 1%;
        font-family: 'Inter', sans-serif;
    }

    .directory{
        margin: 1.5% -1%;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
    }

    .directory-content{
        padding: 1.5%;
        display: flex;
        align-items: center;
    }

    .select-directory{
        color: black;
        text-decoration: none;
    }

    .select-directory:hover{
        cursor: pointer;
    }

    .logo{
        width: 70px;
        height: 70px;
    }

    .directory-title{
        margin: 0% 0% 0% 2%;
        width: 100%;
        font-weight: 600;
        font-size: 25px;
    }

    .directory:hover{
        color: #B90321;
        background-color: #f4f4f4;

        .logo{
            filter: invert(8%) sepia(80%) saturate(5145%) hue-rotate(2deg) brightness(98%) contrast(114%);
        }
    }   
</style>