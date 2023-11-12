<template>
    <title>Eligible Voters - COMELEC Portal</title>
    <Navbar></Navbar>

    <div class="header row my-4">
        <div class="col-9">
            <h1 class="eligible">
                <span class="return" @click="returnPage">Directory</span>&nbsp;>&nbsp;Eligible Voters
            </h1>
        </div>
        <div class="col-3">
            <input class="searchbar" type="text" v-model="searchQuery" placeholder="Search voters...">
        </div>
    </div>
    
    <div class="parent">
        <BaseTable class="item-table" 
                :columns="['Student Name', 'Course']" 
                :columnWidths="['50%', '50%']"
                :tableHeight="'auto'"
                :maxTableHeight="'755px'">
            <!-- Modify the v-for directive to loop over the filtered list -->
            <tr v-for="(voter, index) in filteredVoters" :key="index">
                <td style="width: 50%; text-align: left; padding-left: 20.3%;" class="my-cell">{{ voter.LastName + ", " + voter.FirstName + (voter.MiddleName ? " " + voter.MiddleName : "") }}</td>
                <td style="width: 50%;" class="my-cell">{{ voter.Course }}</td>
            </tr>
        </BaseTable>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed } from 'vue';
    import axios from 'axios';

    export default {
        setup() {
            const fetchVotersData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/all/arranged`, {
                });
                console.log(`Get all voters successful. Duration: ${response.duration}ms`)

                return response.data.students
            }

            const { data: votersData,
                    isLoading: isVotersLoading,
                    isSuccess: isVotersSuccess,
                    isError: isVotersError} =
                    useQuery({
                        queryKey: ['fetchVotersData'],
                        queryFn: fetchVotersData,
                    })

            // Add a ref for the search query
            const searchQuery = ref('');

            // Add a computed property that returns the filtered list
            const filteredVoters = computed(() => {
                if (!searchQuery.value) {
                    return votersData.value;
                }
                const searchQueryNormalized = searchQuery.value.replace(/,| /g, '').toLowerCase();
                return votersData.value.filter(voter => {
                    const fullName1 = `${voter.LastName}${voter.FirstName}${voter.MiddleName ? voter.MiddleName : ""}`.replace(/,| /g, '').toLowerCase();
                    const fullName2 = `${voter.FirstName}${voter.MiddleName ? voter.MiddleName : ""}${voter.LastName}`.replace(/,| /g, '').toLowerCase();
                    return fullName1.includes(searchQueryNormalized) || fullName2.includes(searchQueryNormalized);
                });
            });

            return {
                votersData,
                isVotersLoading,
                isVotersSuccess,
                isVotersError,
                
                searchQuery,  // Make sure to return these
                filteredVoters
            }
           
        },
        components: {
            Standards,
            Navbar,
            BaseContainer,
            BaseTable
        },
        methods: {
            returnPage(){
                router.visit('/directory')
            }
        }
    }
</script>

<style scoped>
    .eligible{
        font-size: 28px;
        font-weight: 800;
    }

    .header{
        margin-left: 14.3%;
        width: 78%;
    }

    .return{
        font-size: 28px;
        font-weight: 800;
        color: #B90321;
    }

    .return:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .searchbar  {
        width: 60%;
        padding: 7px;
        border-radius: 8px;
        outline: none;
        border: 1px solid rgba(40, 40, 40, 0.25);

        transition: border 0.15s ease-out;
    }

    .searchbar:focus {
        border: 1px solid rgba(13, 13, 13, 0.561)
    }

    .parent{
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .item-table{
        width: 70%;
    }

</style>