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
        
        <BaseContainer :height="'auto'" :maxHeight="'400px'">
            <div class="utilities">
               <SearchBarAndFilter :options="options"></SearchBarAndFilter>
            </div>

            <BaseTable class="item-table" 
                :columns="['ID', 'Name', 'School Year', 'Created By', 'Date Created']" 
                :columnWidths=columnWidths
                :tableHeight="'auto'"
                :maxTableHeight="'300px'">
                <tr v-for="(item, index) in items" :key="index" @click="selectItem(item)">
                    <td v-for="(value, key, i) in itemsWithoutId[0]" 
                        :key="key" 
                        :style="{ width: columnWidths[i] }" 
                        class="my-cell">{{ item[key] }}
                    </td>
                </tr>

            </BaseTable>
        </BaseContainer>
    </div>
</template>

<script>
    import { useUserStore } from '../../Stores/UserStore';
    import { router } from '@inertiajs/vue3'
    import { ref } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import SearchBarAndFilter from '../../Shared/SearchBarAndFilter.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';

    import axios from 'axios';

    export default {
        setup(props) {
            const userStore = useUserStore();
            userStore.id = props.organization_id;
            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            userStore.user_role = props.user_role;
            userStore.organization_name = props.organization_name;
            userStore.organization_position_id = props.officer_position_id;

            const organization_name = props.organization_name;
            
            const options = [
                { text: 'Name', value: 'name' },
                { text: 'School Year', value: 'school-year' },
                { text: 'Created By', value: 'created-by' },
            ];

            const items = ref([]);
            const columnWidths = ['10%', '20%', '20%', '20%', '20%'];

            return {options, 
                    items,
                    columnWidths,
                    organization_name,}
        },
        created() {
            this.fetchTableData();
        },
        computed: {
            itemsWithoutId() {
                return this.items.map(item => {
                    let newItem = { ...item };
                    delete newItem.id;
                    return newItem;
                });
            }
        },
        components: { Navbar, Sidebar, ActionButton, SearchBarAndFilter, BaseContainer, BaseTable, },
        props: {
            student_number: String,
            organization_id: Number,
            organization_name: String,
            officer_position_id: Number,
            user_role: String,
            full_name: String,
        },
        methods: {
            createElectionRedirect(){
                router.visit('/organization/elections/create');
            },
            fetchTableData() {
                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/organization/all`, {
                        name: this.organization_name,
                    })
                    .then(response => {
                        console.log(`Elections table fetched successfully. Duration: ${response.duration}`)

                        const elections = response.data.elections.map(item => {
                            let date_created = new Date(item.created_at);
                            let formattedDate = date_created.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

                            return {
                                id: item.ElectionId,
                                count: item.count,
                                name: item.ElectionName,
                                school_year: item.SchoolYear,
                                created_by_name: item.CreatedByName,
                                date_created: formattedDate,
                            }
                        });

                        this.items = [...elections];
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            selectItem(item) {
                router.visit(`/organization/elections/view`, {
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