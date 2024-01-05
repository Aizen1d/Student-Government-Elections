<template>
    <title>Directory Candidates Selection - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <div class="header row">
        <div class="col">
            <h1 class="eligible">
                <span class="return" @click="returnPage">Directory</span>&nbsp;>&nbsp;Election Selection
            </h1>
        </div>
    </div>

    <div v-if="isElectionsLoading" style="text-align: center;">
        <h1 style="color: black;">Loading..</h1>
    </div>

    <div class="parent" v-if="!isElectionsLoading">
        <BaseTable class="item-table" v-if="atleastOneElection"
                :columns="['Organization', 'Election Title']" 
                :columnWidths="['30%', '50%', '20%']"
                :tableHeight="'auto'"
                :maxTableHeight="'235px'">
            <tr v-for="(election, index) in electionsData" :key="index" @click="selectItem(election)">
                <td style="width: 30%; text-align: left; padding-left: 14.6%;" class="my-cell">{{ election.type }}</td>
                <td style="width: 50%; text-align: left; padding-left: 27%;" class="my-cell">{{ election.name }}</td>
            </tr>
        </BaseTable>
        <div v-else>
            <h1 class="my-4">There are no elections and candidates at the moment.</h1>
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
                    type: election.StudentOrganizationName,
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
                router.visit(`/directory/candidates/view`, { 
                    data: { 
                            id: item.id 
                        }
                });
            },
            returnPage(){
                router.visit('/directory')
            }
        },
    }
</script>

<style scoped>
    .return{
        font-size: 28px;
        font-weight: 800;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .eligible{
        font-size: 28px;
        font-weight: 800;
    }

    .header{
        margin-top: 1%;
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