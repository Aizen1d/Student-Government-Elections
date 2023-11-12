<template>
    <title>Queues List - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2 class="my-1">
                    <span class="return" @click="returnPage">Voters Registration</span> > Queues
                </h2>            
            </div>
        </div>   
        
        <BaseContainer class="item-container" :height="'auto'" :maxHeight="'500px'">
            <BaseTable class="item-table" 
                    :columns="['Queue Name', 'To Email Total', 'Email Sent', 'Email Failed', 'Status', 'Created At']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'280px'">
                <tr v-for="(item, index) in queueData" :key="index">
                    <td class="my-cell">{{ item.QueueName }}</td>
                    <td class="my-cell">{{ item.ToEmailTotal }}</td>
                    <td class="my-cell">{{ item.EmailSent }}</td>
                    <td class="my-cell">{{ item.EmailFailed }}</td>
                    <td class="my-cell">{{ item.Status }}</td>
                    <td class="my-cell">{{ formatDate(item.created_at) }}</td>
                </tr>
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

    export default {
        setup() {

            const fetchQueuesData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/insert/data/queues/all`);

                return response.data.queues
            }

            const { data: queueData, 
                isLoading: isQueueLoading,
                isSuccess: isQueueSuccess,
                isError: isQueueError } = 
                useQuery({
                    queryKey: ['fetchQueuesData'],
                    queryFn: fetchQueuesData,
                    refetchInterval: 1000,
                });

            setInterval(() => {
                console.log(queueData);
            }, 1000);

            return {
                queueData,
                isQueueLoading,
                isQueueSuccess,
                isQueueError,
            }
        },
        components: { Navbar, Sidebar, ActionButton, SearchBarAndFilter, BaseContainer, BaseTable, },
        methods: {
            returnPage() {
                router.visit('/comelec/voters-registration');
            },
            formatDate(date) {
                let options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(date).toLocaleDateString(undefined, options);
            },
        }
    }
</script>

<style scoped>
.return{
    cursor: pointer;
    color: #B90321;
}

.return:hover{
    text-decoration: underline;
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