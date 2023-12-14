<template>
    <title>Directory Certifications - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h1 class="page-title">Certifications</h1>
            <button @click="createCertification" class="create-button">Create</button>
        </div>
        
        <div class="list">
            <table class="table table-hover table-bordered border-dark table-responsive">
                <thead class="head">
                    <tr>
                        <th>#</th>
                        <th class="th-sm">Title</th>
                        <th class="th-sm">Date Created</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th scope="row">1</th>
                        <th>Oath of Certification</th>
                        <th>September 4, 2023</th>
                    </tr>
                    <tr>
                        <th scope="row">2</th>
                        <th>Certification</th>
                        <th>September 4, 2023</th>
                    </tr>
                </tbody>
            </table>
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
            createCertification(){
                router.visit('/comelec/directory/certifications/create');
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

    .page-title{
        font-weight: 900;
        font-size: 28px;
        margin: 0%;
    }

    .create-button{
        padding: 13px 50px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
    }

    .list{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1% 0% -1%;
        padding: 30px 30px 15px 30px;
        border-radius: 7px;
        max-height: 550px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }
</style>