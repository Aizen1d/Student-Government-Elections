<template>
    <title>Directory Student Organization View - COMELEC Portal</title>
    <Navbar></Navbar>
    
    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">Directory</span> 
            <span class="arrow"> > </span>
            <span class="header" @click.prevent="returnPage">Select Student Organization</span> 
            <span class="arrow"> > </span>
            View
        </h1>

        <template v-if="!isOrganizationLoading">
            <div class="organization-header">
                <img src="ssc.png" alt="" class="organization-logo">
                <h1 class="organization-name mt-2">{{ organizationData.OrganizationName }}</h1>
                <div style="margin-left: auto;">
                    <span class="requirements"><strong>Course Requirements</strong>: {{ organizationData.OrganizationMemberRequirements }}</span>
                </div>
            </div>

            <hr class="line">

            <div class="components">
                <div class="organization-adviser">
                    <div class="adviser-wrapper">
                        <div class="adviser-information">
                            <img :src="organizationData.AdviserImage" alt="" class="adviser-img">
                            <h6 class="adviser-name">{{ organizationData.AdviserName }}</h6>
                            <span class="adviser-label">Adviser</span>
                        </div>
                    </div>
                </div>

                <div class="organization">
                    <div class="organization-wrapper">
                        <div class="organization-information">
                            <span class="label">VISION</span> <hr class="divider">
                            <p class="information mb-3">
                                {{ organizationData.Vision }}
                            </p>

                            <span class="label">MISSION</span> <hr class="divider">
                            <p class="information">
                                {{ organizationData.Mission }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="people">
                <div class="organization-members">
                    <div class="organization-member-wrapper">
                        <h1 class="officer-header">Organization Officers</h1>

                        <hr class="divider">

                        <div class="member" v-for="(officer, index) in organizationData.officers" :key="index">
                            <div class="member-wrapper">
                                <img :src="officer.Image" alt="" class="officer-img">
                                <div class="member-information">
                                    <span class="member-name">{{ officer.FirstName + " " + (officer.MiddleName ? officer.MiddleName + " " : "") + officer.LastName }}</span>
                                    <span class="member-position">{{ officer.Position }}</span>
                                    <span class="member-course">{{ officer.CourseCode }} {{ officer.Year }}-{{ officer.Section }}</span>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="member-table">
                    <div class="table-wrapper">
                        <h1 class="officer-header">Organization Members</h1>

                        <hr class="divider">
                        
                        <div class="voter-list">
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                    <th scope="col"><span class="table-padding1">STUDENT NAME</span></th>
                                    <th scope="col"><span class="table-padding1 center">COURSE</span></th>
                                    <th scope="col"><span class="table-padding1 center">YEAR & SECTION</span></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="(member, index) in organizationData.members">
                                    <td><span class="table-padding">{{ member.FirstName + " " + (member.MiddleName ? member.MiddleName + " " : "") + member.LastName }}</span></td>
                                    <td><span class="table-padding center">{{ member.CourseCode }}</span></td>
                                    <td><span class="table-padding center">{{ member.Year }}-{{ member.Section }}</span></td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </template>
        
    </main>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import BaseContainer from '../Shared/BaseContainer.vue'
    import BaseTable from '../Shared/BaseTable.vue'

    import { ref, watch } from 'vue'
    import axios from 'axios'
    import { useQuery } from '@tanstack/vue-query'
    import { router } from '@inertiajs/vue3'

    export default {
        setup(props){
            const organizationId = ref(Number(props.id));

            const fetchStudentOrganization = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/organization/${organizationId.value}`, {
                });
                console.log(`Get organization id ${organizationId.value}. Duration: ${response.duration}ms`)

                return response.data.student_organization;
            }

            const { data: organizationData,
                    isLoading: isOrganizationLoading,
                    isSuccess: isOrganizationSuccess,
                    isError: isOrganizationError} =
                    useQuery({
                        queryKey: [`fetchStudentOrganization${organizationId.value}`],
                        queryFn: fetchStudentOrganization,
                    })

            return{
                organizationData,
                isOrganizationLoading,
                isOrganizationSuccess,
                isOrganizationError,
            }
        },
        components:{
            Standards,
            Navbar,
            BaseContainer,
            BaseTable,
        },
        props:{
            id: ''
        },
        methods:{
            returnSelection(){
                router.visit('/directory/student-organization')
            },
        },
    }
</script>

<style scoped>
    .main-margin{
        margin: 0% 8%;
    }

    .header{
        margin: 1.5% 0%;
        font-size: 28px;
        font-weight: bold;
    }

    .current-page{
        color: #800000;
    }

    .organization-header{
        display: flex;
        align-items: center;
    }

    .organization-logo{
        width: 75px;
    }

    .organization-name{
        margin-left: 1.5% !important;
        font-size: 30px;
        font-weight: bolder;
        margin: 0;
        color: #800000;
    }

    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 2% 0%;
    }

    .divider{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
    }

    .requirements{
        font-size: 18px;
    }

    .components{
        display: flex;
        width: 100%;
        height: 500px;
    }

    .organization-adviser{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        width: 400px;
    }

    .adviser-wrapper{
        padding: 5%;
        height: 100%;
    }

    .adviser-information{
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }

    .adviser-information:hover{
        color: #800000;
    }

    .adviser-img{
        border-radius: 6px;
        width: 100%;
        height: 400px;
        object-fit: cover;
    }

    .adviser-name{
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin: 3% 0%;
    }

    .adviser-label{
        font-size: 18px;
        margin: auto;
    }

    .organization{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        width: 100%;
        margin-left: 2%;
        display: flex;
    }

    .organization-information{
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
    }

    .organization-wrapper{
        padding: 4%;
        height: 100%;
    }

    .label{
        font-size: 20px;
        font-weight: bold;
    }

    .information{
        font-size: 18px;
        text-indent: 70px;
        margin: 0;
    }

    .people{
        margin: 2% 0%;
        display: flex;
    }

    .organization-members{
        width: 70%;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
    }

    .organization-member-wrapper{
        padding: 5%;
    }

    .member-wrapper{
        padding: 3%;
        display: flex;
        align-items: center;
    }

    .member{
        width: 100%;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
    }

    .member-information{
        margin-left: 3.5%;
        display: flex;
        flex-direction: column;
    }

    .member-name{
        font-size: 18px;
        font-weight: bold;
    }

    .member-position{
        font-size: 18px;
        margin: 5% 0%;
    }

    .member-course{
        font-size: 18px;
    }

    .officer-img{
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
    }

    .officer-header{
        font-size: 22px;
        font-weight: bold;
    }

    .member-table{
        margin-left: 2%;
        width: 100%;
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 6px;
        height: max-content;
    }

    .table-wrapper{
        padding: 3.5%;
    }

    .form-control{
        font-size: 18px;
    }

    .search{
        width: 30%;
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
</style>