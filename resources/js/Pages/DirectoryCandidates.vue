<template>
    <title>Directory Candidates Selection - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">Directory</span> 
            <span class="arrow"> > Candidates ></span>
            Select Election
        </h1>

        <div v-for="(election, index) in electionsData" :key="index" @click="selectItem(election)">
            <div class="select">
                <div class="election">
                    <div class="election-wrapper">
                        <img :src="election.OrganizationLogo" alt="" class="election-img">
                        <span class="election-name">{{ election.ElectionName }}</span>
                    </div>
                </div>
            </div>
        </div>

    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'

    import { ref, watch } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'

    export default {
        setup(props){
            const atleastOneElection = ref(false);

            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`, {
                });
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                if (response.data.elections.length > 0){
                    atleastOneElection.value = true;
                }
                else {
                    atleastOneElection.value = false;
                }           

                return response.data.elections.map(election => {
                    const logo_url = `${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/get/cached/elections/${election.OrganizationLogo}`
                    election.OrganizationLogo = logo_url;

                    return election;
                });
            }

            const { data: electionsData,
                    isLoading: isElectionsLoading,
                    isSuccess: isElectionsSuccess,
                    isError: isElectionsError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            return{
                atleastOneElection,

                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,
            }
        },
        components:{
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
        },
        methods:{
            selectItem(item){
                console.log(item);
                router.visit(`/directory/candidates/view`, { 
                    data: { 
                            id: item.ElectionId
                        }
                });
            },
            returnPage(){
                router.visit('/directory')
            },
        },
    }
</script>

<style scoped>
     .main{
        margin: 3% 5%;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .current-page{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: #800000 !important;
    }

    .arrow{
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .main-margin{
        margin: 0% 8%;
    }

    .current-page{
        color: #800000;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
    }

    .election{
        margin: 1.5% 0;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
    }

    .election-wrapper{
        padding: 1%;
        display: flex;
        align-items: center;
    }

    .select{
        color: black;
        text-decoration: none;
    }

    .select:hover{
        cursor: pointer;
    }

    .election-img{
        width: 55px;
        height: 55px;
    }

    .election-name{
        margin-left: 2%;
        width: 100%;
        font-weight: 600;
        font-size: 25px;
    }

    .election:hover{
        color: #800000;
        background-color: #f4f4f4;
    }   
</style>