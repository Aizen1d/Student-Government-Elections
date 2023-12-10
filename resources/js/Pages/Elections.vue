<template>
    <title>Elections - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <div class="main">
        <img src="../../images/Home/comelec.jpg" alt="" class="main-ann">
    </div>
    
    <div class="header row">
        <div class="col">
            <h1 class="eligible">
                ELECTIONS
            </h1>
        </div>
    </div>

    <div class="parent">
        <BaseTable class="item-table" v-if="atleastOneElection" 
                :columns="['Organization', 'Election Title', 'Election Period']" 
                :columnWidths="['50%', '50%', '50%']"
                :tableHeight="'auto'"
                :maxTableHeight="'235px'">
            <tr v-for="(election, index) in electionsData" :key="index" @click="selectItem(election)">
                <td style="width: 50%; text-align: left; padding-left: 12.5%;" class="my-cell">{{ election.type }}</td>
                <td style="width: 50%; text-align: left; padding-left: 12.5%;" class="my-cell">{{ election.name }}</td>
                <td style="width: 50%; text-align: left; padding-left: 11.5%;" class="my-cell">{{ election.period }}</td>
            </tr>
        </BaseTable>
        <div v-else>
            <h1 class="my-5">No elections are currently happening at the moment.</h1>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'

    import { ref } from 'vue'
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

                const elections = response.data.elections.map(election => ({
                    id: election.ElectionId,
                    name: election.ElectionName,
                    type: election.ElectionType,
                    status: election.ElectionStatus,
                    period: election.ElectionPeriod,
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
                router.visit(`/elections/view`, { 
                    data: { 
                            id: item.id 
                        }
                });
            }
        },
    }
</script>

<style scoped>
    .eligible{
        font-size: 35px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .header{
        margin-top: -8.5%;
        margin-bottom: 1%;
        margin-left: 14.3%;
        width: 78%;
    }

    .parent{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .item-container{
        width: 70%;
        margin-top: 2%;
    }

    .main{
        height: 500px;
    }

    .main-ann{
        width: 100%;
        height: 60%;
        object-fit: cover;
    }

    .item-table{
        width: 70%;
    }
</style>