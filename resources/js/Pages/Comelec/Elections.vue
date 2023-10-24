<template>
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
               <SearchBarAndFilter :options="options"></SearchBarAndFilter>
            </div>

            <BaseTable class="item-table" 
                :columns="['ID', 'Name', 'Type', 'School Year', 'Created By', 'Date Created', 'Status']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'300px'">
                <tr v-for="(item, index) in items.value" :key="index" @click="selectItem(item)">
                    <td v-for="(value, key, i) in itemsWithoutId[index]"
                        :key="key"
                        :style="{ width: columnWidths[i] }" 
                        class="my-cell">{{ value }}
                    </td>
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
                { text: 'Name', value: 'name' },
                { text: 'Type', value: 'type' },
                { text: 'School Year', value: 'school-year' },
                { text: 'Created By', value: 'created-by' },
            ];

            const items = ref([]);
            const columnWidths = ['10%', '20%', '20%', '20%', '20%', '20%', '20%'];
            
            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`);
                console.log(`Elections table fetched successfully. Duration: ${response.duration}`)

                const elections = response.data.elections.map(item => {
                    let date_created = new Date(item.created_at);
                    let formattedDate = date_created.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

                    return {
                        id: item.ElectionId,
                        count: item.count,
                        name: item.ElectionName,
                        type: item.ElectionType,
                        school_year: item.SchoolYear,
                        created_by_name: item.CreatedByName,
                        date_created: formattedDate,
                        status: item.ElectionStatus,
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

            return {options, 
                    items,
                    columnWidths,
                    
                    electionsData,
                    isLoading,
                    isSuccess,
                    isError,
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
            selectItem(item) {
                router.visit(`/comelec/elections/view`, {
                    data: {
                        id: item.id,
                    }
                });
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