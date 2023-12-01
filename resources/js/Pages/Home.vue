<template>
    <Navbar></Navbar>
    <div class="main">
        <h1 class="header-label">ELECTIONS</h1>

        <template v-if="atleastOneElection && !isElectionsLoading" v-for="(election, index) in electionsData" :key="index">
            <div class="select-election" @click="electionSelected(election)">
                <div class="election">
                    <div class="election-content">
                        <img src="" alt="?" class="organization-logo">
                        <h1 class="election-title">{{ election.name }}</h1>
                    </div>
                </div>
            </div>
        </template>
        <div v-if="!atleastOneElection && !isElectionsLoading">
            <h1>No elections are currently happening at the moment.</h1>
        </div>

    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';
    import { useUserStore } from '../Stores/UserStore.js';

    import { ref } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'
    import { useLocalStorage } from '@vueuse/core';

    export default {
        setup(props) {
            const userStore = useUserStore();
            const atleastOneElection = ref(useLocalStorage('atleastOneElection', false));

            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            
            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`, {
                });
                console.log(`Get all elections successful. Duration: ${response.duration}ms`)

                const elections = response.data.elections.map(election => ({
                    id: election.ElectionId,
                    name: election.ElectionName,
                    type: election.ElectionType,
                    status: election.ElectionStatus,
                }));

                if (response.data.elections.length > 0){
                    atleastOneElection.value = true;
                }
                else {
                    atleastOneElection.value = false;
                }

                return elections;
            }

            const { data: electionsData,
                    isLoading: isElectionsLoading,
                    isSuccess: isElectionsSuccess,
                    isError: isElectionsError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            return {
                atleastOneElection,
                electionsData,
                isElectionsLoading,
                isElectionsSuccess,
                isElectionsError,
            };
        },
        components: { Navbar },
        props: {
            student_number: '',
            full_name: '',
        },
        methods: {
            electionSelected(election){
                router.visit('/voting/process', {
                    data: {
                        id: election.id,
                    }
                })
            }
        }
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

    .select-election:hover{
        cursor: pointer;
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