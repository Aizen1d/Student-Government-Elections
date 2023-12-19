<template>
    <title>Directory Certifications - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h2 class="my-1">
                <span class="return" @click="returnPage">Directory</span> > Certifications
            </h2>
            <ActionButton @click="createCertification" class="create-button">Create</ActionButton>
        </div>
     
        <BaseContainer class="item-container" :height="'auto'" :maxHeight="'550px'">
            <BaseTable class="item-table" 
                    :columns="['ID', 'Certification Title', 'Election Name', 'Date']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'500px'">
                <tr v-for="(certification, index) in certificationsData" :key="index" @click="selectItem(item)">
                    <td class="my-cell">{{ index + 1 }}</td>
                    <td class="my-cell">{{ certification.Title }}</td>
                    <td class="my-cell">{{ certification.ElectionName }}</td>
                    <td class="my-cell">{{ toDate(certification.Date) }}</td>
                </tr>
            </BaseTable>
        </BaseContainer>

    </div>
</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watch, watchEffect } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import ImageSkeleton from '../../Skeletons/ImageSkeleton.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup() {
            const fetchCertifications = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/certification/all`)
                console.log(`Certifications successfully fetched. Duration: ${response.duration}`)

                return response.data.certifications;
            };

            const { data: certificationsData, isLoading, isSuccess, isError } = 
                useQuery({
                    queryKey: ['fetchCertifications'],
                    queryFn: fetchCertifications,
                });

            return {
                certificationsData,
                isLoading,
                isSuccess,
                isError,
            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            BaseContainer,
            BaseTable,
            ImageSkeleton,
        },
        methods: {
            returnPage(){
                router.visit('/comelec/directory');
            },
            createCertification(){
                router.visit('/comelec/directory/certifications/create');
            },
            toDate(date){
                return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            },
        }
    }
</script>

<style scoped>
   .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Inter', sans-serif;
        margin-right: 3%;
    }

    .return{
        color: #B90321;
        cursor: pointer;
    }

    .return:hover{
        text-decoration: underline;
    }

    .header{
        display: flex;
        align-items: center;
        margin: 0% -1%;
        justify-content: space-between;
    }

    .page-title{
        font-weight: 900;
        font-size: 28px;
        margin: 0%;
    }

    .list{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1% 0% -1%;
        padding: 30px 30px 15px 30px;
        border-radius: 7px;
        max-height: 550px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }
</style>