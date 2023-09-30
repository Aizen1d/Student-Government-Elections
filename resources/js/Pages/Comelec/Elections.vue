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
        
        <BaseContainer :height="'auto'">
            <div class="utilities">
               <SearchBarAndFilter :options="options"></SearchBarAndFilter>
            </div>

            <BaseTable class="item-table" :columns="['ID', 'Type', 'Name', 'Date Created']" :table-height="'235px'">
                <tr v-for="(item, index) in items" :key="index" @click="selectItem(item)" 
                    v-bind:class="{ 'active-row': selectedItem && selectedItem.id === item.id && selectedItem.announcement_type === item.announcement_type }">
                    <td class="my-cell">{{ item.count }}</td>
                    <td class="my-cell">{{ item.announcement_type.charAt(0).toUpperCase() + item.announcement_type.slice(1) }}</td>
                    <td class="my-cell">{{ item.title }}</td>
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
            // Since this is the landing page for the Comelec after loggin in,
            // We need to set the user's role to comelec in the user store
            const userStore = useUserStore();
            userStore.id = props.comelec_id;
            userStore.student_number = props.student_number;
            userStore.full_name = props.full_name;
            userStore.user_role = props.user_role;
            
            const options = [
                { text: 'Semester', value: 'semester' },
                { text: 'School Year', value: 'school-year' },
            ];

            const items = ref([]);

            return {options, 
                    items,}
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