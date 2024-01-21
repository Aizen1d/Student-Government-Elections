<template>
    <title>Eligible Voters - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnDirectory">Directory</span> 
            <span class="arrow"> > Eligible Voters ></span>
            <span class="arrow return-selection" @click.prevent="returnSelection"> Select Election</span>
            
            <span class="arrow"> ></span>
            View Eligible Voters
        </h1>

        <div class="election">
            <div class="election-wrapper">
                <div class="election-header">
                    <div class="centered">
                        <span class="election-title">{{ activeElectionName }}</span>
                    </div>
                </div>

                <hr class="line">
                
                <div class="search">
                    <div class="input-container">
                        <input class="form-control" type="search" v-model="searchQuery" placeholder="Search voters..." aria-label="Search">
                    </div>
                </div>
                
                <div class="voter-list">
                    <table class="table table-striped">
                        <thead>
                          <tr>
                            <th scope="col"><span class="table-padding1">STUDENT NAME</span></th>
                            <th scope="col"><span class="table-padding1 center">COURSE</span></th>
                            <th scope="col"><span class="table-padding1 center">YEAR & SECTION</span></th>
                          </tr>
                        </thead>
                        <tbody v-for="(students, courseCode) in filteredVoters" :key="courseCode">
                          <tr v-for="student in students" :key="student.StudentNumber">
                            <td><span class="table-padding">{{ student.LastName }} {{ student.FirstName }} {{ student.MiddleName ? student.MiddleName : '' }}</span></td>
                            <td><span class="table-padding center">{{ courseCode }}</span></td>
                            <td><span class="table-padding center">{{ student.Year }}-{{ student.Section }}</span></td>
                          </tr>
                        </tbody>
                    </table>
                </div>
                
            </div>
        </div>
    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue'

    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { ref, computed } from 'vue';
    import axios from 'axios';

    export default {
        setup(props) {
            const activeElectionIndex = ref(Number(props.id));
            const activeElectionName = ref(props.electionName);

            const fetchVotersData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/eligible/all/${activeElectionIndex.value}`, {
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
                let filtered = {};
                for (let course in votersData.value) {
                    filtered[course] = votersData.value[course].filter(student => {
                        const fullName1 = `${student.LastName}${student.FirstName}${student.MiddleName ? student.MiddleName : ""}`.replace(/,| /g, '').toLowerCase();
                        const fullName2 = `${student.FirstName}${student.MiddleName ? student.MiddleName : ""}${student.LastName}`.replace(/,| /g, '').toLowerCase();
                        return fullName1.includes(searchQueryNormalized) || fullName2.includes(searchQueryNormalized);
                    });
                }
                return filtered;
            });

            return {
                activeElectionIndex,
                activeElectionName,

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
            BaseTable,
            ImageSkeleton
        },
        props: {
            id: '',
            electionName: ''
        },
        methods: {
            returnDirectory() {
                router.visit('/directory')
            },
            returnSelection() {
                router.visit('/directory/voters')
            },
        }
    }
</script>

<style scoped>
    .main-margin{
        margin: 0% 8%;
    }

    .current-page{
        color: #800000;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
    }

    .centered{
        display: flex;
        align-items: center;
    }

    .end{
        margin-left: auto;
    }

    .election{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        margin: 1.5% 0%;
    }

    .election-wrapper{
        padding: 2%;
    }

    .election-header{
        align-items: center;
    }

    .election-logo{
        width: 50px;
    }

    .election-title{
        font-size: 30px;
        font-weight: bold;
        color: #800000;
        margin: 0% 1.5%;
    }

    .election-label{
        margin: 0% 1%;
    }

    .header-svg{
        width: 35px;
    }

    .result{
        filter: invert(74%) sepia(72%) saturate(2485%) hue-rotate(349deg) brightness(104%) contrast(88%);
    }

    .header-button{
        border: transparent;
        background-color: transparent;
        align-items: center;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .form-control{
        font-size: 18px;
    }

    .search{
        width: 30%;
        display: flex;
    }

    .input-container {
        position: relative;
        width: 100%;
    }

    .input-container::before {
        content: '';  
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: url('search.svg') no-repeat center;
        background-size: contain;
        width: 20px;
        height: 20px;
        filter: invert(75%) sepia(0%) saturate(132%) hue-rotate(164deg) brightness(91%) contrast(82%);
    }

    .form-control {
        padding-left: 40px;  /* Adjust this value as needed */
        font-size: 18px;
    }

    .voter-list{
        margin-top: 0.5%;
        margin-bottom: -1%;
    }

    .table{
        font-size: 18px;
        align-items: center;
    }

    thead{
        border-bottom: 2px solid #800000;
    }

    .table-padding{
        margin: 0px 50px;
        display: flex;
        height: 40px; /* adjust as needed */
        overflow: hidden;
        align-items: center;
    }

    .table-padding1{
        margin: 0px 50px;
        display: flex;
        height: 40px; /* adjust as needed */
        overflow: hidden;
        align-items: center;
        margin-bottom: 5px;
    }

    .center{
        justify-content: center;
    }

    .current-page{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: #800000 !important;
    }

    .arrow{
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }

    .header:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .return-selection:hover{
        cursor: pointer;
        text-decoration: underline;
    }
</style>