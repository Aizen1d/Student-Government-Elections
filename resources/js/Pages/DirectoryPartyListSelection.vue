<template>
    <title>Directory Partylists Selection - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">Directory</span> 
            <span class="arrow"> > Partylists > </span>
            <span class="arrow"> {{ activeElectionName }} ></span>
            Select Partylist
        </h1>

        <div v-for="(party, index) in partylistData" :key="index" @click="selectItem(party)">
            <div class="select">
                <div class="election">
                    <div class="election-wrapper">
                        <span class="election-name">{{ party.PartyListName }}</span>
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
            const activeElectionIndex = ref(Number(props.id));
            const activeElectionName = ref(props.electionName);
            const atleastOnePartylist = ref(false);

            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/election/${activeElectionIndex.value}/approved/all`, {
                });
                console.log(`Get all partylists with election id ${activeElectionIndex.value} successful. Duration: ${response.duration}ms`)

                if (response.data.partylists.length > 0){
                    atleastOnePartylist.value = true;
                }
                else {
                    atleastOnePartylist.value = false;
                }           

                return response.data.partylists
            }

            const { data: partylistData,
                    isLoading: isPartylistLoading,
                    isSuccess: isPartylistSuccess,
                    isError: isPartylistError} =
                    useQuery({
                        queryKey: ['fetchElectionsTable'],
                        queryFn: fetchElectionsTable,
                    })

            return{
                activeElectionIndex,
                activeElectionName,

                atleastOnePartylist,

                partylistData,
                isPartylistLoading,
                isPartylistSuccess,
                isPartylistError,
            }
        },
        components:{
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
        },
        props: {
            id: '',
            electionName: ''
        },
        methods:{
            selectItem(item){
                console.log(item);
                router.visit(`/directory/partylists/view`, { 
                    data: { 
                            id: item.PartyListId
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