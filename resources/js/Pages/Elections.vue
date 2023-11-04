<template>
    <title>Elections - COMELEC Portal</title>
    <Navbar></Navbar>
    <div class="parent">
        <BaseContainer class="item-container" :height="'300px'" :maxHeight="'335px'">
            <BaseTable class="item-table" 
                    :columns="['Election Name', 'Election Type']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'235px'">
                <tr v-for="(election, index) in electionsData" :key="index" @click="selectItem(election)">
                    <td class="my-cell">{{ election.name }}</td>
                    <td class="my-cell">{{ election.type }}</td>
                </tr>
            </BaseTable>
        </BaseContainer>
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
    .parent{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .item-container{
        width: 70%;
        margin-top: 2%;
    }
</style>