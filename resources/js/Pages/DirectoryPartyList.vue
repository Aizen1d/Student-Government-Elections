<template>
    <title>Directory Partylist Selection - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <div class="header row">
        <div class="col">
            <h1 class="eligible">
                <span class="return" @click="returnPage">Directory</span>&nbsp;>&nbsp;Partylist Selection
            </h1>
        </div>
    </div>

    <div v-if="isPartylistLoading" style="text-align: center;">
        <h1 style="color: black;">Loading..</h1>
    </div>

    <div class="parent" v-if="!isPartylistLoading">
        <BaseTable class="item-table" v-if="atleastOnePartylist"
                :columns="['Partylist Name', 'Election Title', 'Organization']" 
                :columnWidths="['50%', '50%', '50%']"
                :tableHeight="'auto'"
                :maxTableHeight="'235px'">
            <tr v-for="(partylist, index) in partylistData" :key="index" @click="selectItem(partylist)">
                <td style="width: 50%; text-align: left; padding-left: 12%;" class="my-cell">{{ partylist.PartyListName }}</td>
                <td style="width: 50%; text-align: left; padding-left: 12.5%;" class="my-cell">{{ partylist.ElectionName }}</td>
                <td style="width: 50%; text-align: left; padding-left: 12.6%;" class="my-cell">{{ partylist.StudentOrganizationName }}</td>
            </tr>
        </BaseTable>
        <div v-else>
            <h1 class="my-4">(There are no partylists at the moment)</h1>
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
            const atleastOnePartylist = ref(false);

            const fetchPartylistTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/all`, {
                });
                console.log(`Get all partylist successful. Duration: ${response.duration}ms`)

                if (response.data.partylists.length > 0){
                    atleastOnePartylist.value = true;
                }
                else {
                    atleastOnePartylist.value = false;
                }

                return response.data.partylists;
            }

            const { data: partylistData,
                    isLoading: isPartylistLoading,
                    isSuccess: isPartylistSuccess,
                    isError: isPartylistError} =
                    useQuery({
                        queryKey: ['fetchPartylistTable'],
                        queryFn: fetchPartylistTable,
                    })

            return{
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
        methods:{
            selectItem(item){
                router.visit(`/directory/partylists/view`, { 
                    data: { 
                            id: item.PartyListId 
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