<template>
    <title>Approvals - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Approvals</h2>
            </div>    
        </div>   
        
        <BaseContainer :height="'auto'" :maxHeight="'760px'">
            <div class="utilities">
                <div class="row">
                    <div class="col-2">
                        <select class="form-select filter" aria-label="Default select example" v-model="filterType">
                            <option value="" disabled hidden selected>Filter by</option>
                            <option v-for="(option, index) in options" 
                                    :key="index" 
                                    :value="option.value">
                                    {{ option.text }}
                            </option>
                        </select>
                    </div>
                    <div class="col">
                        <h1 v-show="filterType === 'coc'" class="table-data-label">Viewing CoC</h1>
                        <h1 v-show="filterType === 'party-list'" class="table-data-label">Viewing Partylist</h1>
                    </div>
                </div>
            </div>

            <BaseTable class="item-table" 
                :columns="['Student Number', 'Status', 'Date Submitted']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'300px'"
                v-if="filterType === ''">
            </BaseTable>

            <BaseTable class="item-table" 
                :columns="['Student Number', 'Status', 'Date Submitted']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'300px'"
                v-if="!isPartylistLoading && filterType === 'coc'">
                <div>
                    <tr v-for="(item, coc_index) in CoCData" :key="coc_index" @click="selectCoCItem(item)">
                        <td :style="{ width: columnWidths[0] }" class="my-cell">{{ item.StudentNumber }}</td>
                        <td :style="{ width: columnWidths[1] }" class="my-cell">{{ item.Status }}</td>
                        <td :style="{ width: columnWidths[2] }" class="my-cell">{{ formatDate(item.created_at) }}</td>
                    </tr>
                </div>
            </BaseTable>

            <BaseTable class="item-table" 
                :columns="['Party Name', 'Status', 'Date Submitted']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'300px'"
                v-if="!isPartylistLoading && filterType === 'party-list'">
                <div>
                    <tr v-for="(item, index) in partylistData" :key="index" @click="selectPartyItem(item)">
                        <td :style="{ width: columnWidths[0] }" class="my-cell">{{ item.PartyListName }}</td>
                        <td :style="{ width: columnWidths[1] }" class="my-cell">{{ item.Status }}</td>
                        <td :style="{ width: columnWidths[2] }" class="my-cell">{{ formatDate(item.created_at) }}</td>
                    </tr>
                </div>
            </BaseTable>

        </BaseContainer>
    </div>
</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watchEffect, computed } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import SearchBarAndFilter from '../../Shared/SearchBarAndFilter.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';

    import axios from 'axios';

    import { useQuery } from "@tanstack/vue-query";
    import { useLocalStorage } from '@vueuse/core';

    export default {
        setup() {
            const filterType = useLocalStorage('approvalsFilterType', '');

            const options = [
                { text: 'CoC', value: 'coc' },
                { text: 'Party List', value: 'party-list' },
            ];

            const columnWidths = ['35%', '30%', '35%'];

            const fetchCoCData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/coc/all`);
                console.log(`CoC table fetched successfully. Duration: ${response.duration}`)

                return response.data.coc;
            }

            const fetchPartylistData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/all`);
                console.log(`Partylist table fetched successfully. Duration: ${response.duration}`)

                return response.data.partylists;
            }

            const { data: CoCData,
                    isLoading: isCoCLoading,
                    isError: isCoCError,
                    error: CoCError } = 
                    useQuery({
                        queryKey: ['fetchCoCData'],
                        queryFn: fetchCoCData,
                    })

            const { data: partylistData,
                    isLoading: isPartylistLoading,
                    isError: isPartylistError,
                    error: partylistError } = 
                    useQuery({
                        queryKey: ['fetchPartylistData'],
                        queryFn: fetchPartylistData,
                    })

            return {
                filterType,
                options,
                columnWidths,

                CoCData,
                isCoCLoading,
                isCoCError,
                CoCError,

                partylistData,
                isPartylistLoading,
                isPartylistError,
                partylistError,
            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            SearchBarAndFilter,
            BaseContainer,
            BaseTable
        },
        methods: {
            formatDate(date) {
                let options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(date).toLocaleDateString(undefined, options);
            },
            selectCoCItem(item) {
                router.visit(`/comelec/approvals/view`, {
                    data: {
                        type: 'coc',
                        id: item.CoCId,
                    }
                });
            },
            selectPartyItem(item) {
                router.visit(`/comelec/approvals/view`, {
                    data: {
                        type: 'party-list',
                        id: item.PartyListId,
                    }
                });
            },
        }
    }

</script>

<style scoped>
    .filter{
        width: 100%;
        height: 40px;
        border-radius: 8px;
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .table-data-label{
        font-family: 'Source Sans', sans-serif;
        font-weight: 800;
        font-size: 22px;
        color: #B90321;
        margin-top: .5%;
        align-items: center;
    }

    .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Source Sans', sans-serif;
        margin-right: 3.2%;
    }

    .components h2{
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 1.5%;
    }

    .form-select {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .new{
        text-align: end;
    }

    .new-btn{
        margin-top: -.5%;
    }

    .new-btn:disabled{
        background-color: #cccccc;
    }
    .utilities{
        margin-bottom: 2%;
    }
</style>