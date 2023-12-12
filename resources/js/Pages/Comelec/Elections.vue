<template>
    <title>Elections - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Elections</h2>
            </div>
            <div class="col-6 new">
                <ActionButton @click="createElectionRedirect" class="new-btn">Create Election</ActionButton>
            </div>      
        </div>   
        
        <BaseContainer :height="'auto'" :maxHeight="'760px'">
            <div class="utilities">
                <SearchBarAndFilter :options="options" @filter-changed="filterElections"></SearchBarAndFilter>
            </div>

            <BaseTable class="item-table" 
                :columns="['ID', 'Title', 'Organization', 'School Year', 'Created By', 'Start of Election', 'Date Created', 'Period']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'550px'">
                <tr v-for="(item, index) in filteredElections" :key="index" @click="selectItem(item)">
                    <td :style="{ width: columnWidths[0] }" class="my-cell">{{ item.count }}</td>
                    <td :style="{ width: columnWidths[1] }" class="my-cell">{{ item.title }}</td>
                    <td :style="{ width: columnWidths[2] }" class="my-cell">{{ item.organization }}</td>
                    <td :style="{ width: columnWidths[3] }" class="my-cell">{{ item.school_year }}</td>
                    <td :style="{ width: columnWidths[4] }" class="my-cell">{{ item.created_by_name }}</td>
                    <td :style="{ width: columnWidths[5] }" class="my-cell">{{ item.election_start }}</td>
                    <td :style="{ width: columnWidths[6] }" class="my-cell">{{ item.date_created }}</td>
                    <td :style="{ width: columnWidths[7] }" class="my-cell">{{ item.period }}</td>
                </tr>

            </BaseTable>
        </BaseContainer>
    </div>
</template>

<script>
    import { useUserStore } from '../../Stores/UserStore';
    import { router } from '@inertiajs/vue3'
    import { ref, watchEffect, computed } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import SearchBarAndFilter from '../../Shared/SearchBarAndFilter.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';

    import axios from 'axios';

    import { useQuery, useMutation, useQueryClient  } from "@tanstack/vue-query";

    export default {
        setup(props) {
            // Since this is the landing page for the Comelec after loggin in,
            // We need to set the user's role to comelec in the user store
            const userStore = useUserStore();
            userStore.id = props.comelec_id;
            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            userStore.user_role = props.user_role;
            
            const options = [
                { text: 'Title', value: 'title' },
                { text: 'Organization', value: 'organization' },
                { text: 'School Year', value: 'school-year' },
                { text: 'Created By', value: 'created-by' },
            ];
            const selectedOption = ref('');
            const searchQuery = ref('');

            const items = ref([]);
            const columnWidths = ['10%', '20%', '20%', '20%', '20%', '20%', '20%', '10%'];
            
            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`);
                console.log(`Elections table fetched successfully. Duration: ${response.duration}`)

                const elections = response.data.elections.map(item => {
                    let date_created = new Date(item.created_at);
                    let formattedDate = date_created.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

                    return {
                        id: item.ElectionId,
                        count: item.count,
                        title: item.ElectionName,
                        organization: item.ElectionType,
                        school_year: item.SchoolYear,
                        created_by_name: item.CreatedByName,
                        election_start: new Date(item.ElectionStart).toLocaleString('en-US', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                        date_created: formattedDate,
                        status: item.ElectionStatus,
                        period: item.ElectionPeriod,
                    }
                });

                return elections;
            }

            const { data: electionsData, isLoading, isSuccess, isError, dataUpdatedAt } = 
                useQuery({
                    queryKey: ['fetchElections'],
                    queryFn: fetchElectionsTable,
                });

            watchEffect(() => {
                if (isSuccess) {
                    items.value = electionsData;
                }
            });

            const filteredElections = computed(() => {
                if (!searchQuery.value) {
                    return electionsData.value;
                }

                const searchQueryNormalized = searchQuery.value.replace(/,| /g, '').toLowerCase();

                return electionsData.value.filter(election => {
                    let valueToCheck = '';
                    switch (selectedOption.value) {
                        case 'title':
                            valueToCheck = election.title;
                            break;
                        case 'organization':
                            valueToCheck = election.organization; 
                            break;
                        case 'school-year':
                            valueToCheck = election.school_year;
                            break;
                        case 'created-by':
                            valueToCheck = election.created_by_name;
                            break;
                        default:
                            return true;
                    }

                    const normalizedValueToCheck = valueToCheck.replace(/,| /g, '').toLowerCase();
                    return normalizedValueToCheck.includes(searchQueryNormalized);
                });
            });

            return {options, 
                    selectedOption,
                    searchQuery,
                    items,
                    columnWidths,
                    
                    electionsData,
                    isLoading,
                    isSuccess,
                    isError,

                    filteredElections,
                }
        },
        computed: {
            itemsWithoutId() {
                return this.electionsData.map(item => {
                    let newItem = { ...item };
                    delete newItem.id;
                    return newItem;
                });
            }
        },
        components: { Navbar, Sidebar, ActionButton, SearchBarAndFilter, BaseContainer, BaseTable, },
        props: {
            comelec_id: Number,
            student_number: String,
            full_name: String,
            user_role: String,
        },
        methods: {
            createElectionRedirect(){
                router.visit('/comelec/elections/create');
            },
            formatDate(date) {
                let options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(date).toLocaleDateString(undefined, options);
            },
            selectItem(item) {
                router.visit(`/comelec/elections/view`, {
                    data: {
                        id: item.id,
                    }
                });
            },
            filterElections(filter) {
                this.selectedOption = filter.option;
                this.searchQuery = filter.query;
            }
        }
    }
</script>

<style scoped>
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