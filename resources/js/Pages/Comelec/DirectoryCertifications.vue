<template>
    <title>Directory Certifications - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h2 class="my-1 page-title">
                <span class="return" @click="returnPage">Directory</span> > Certifications
            </h2>
            <ActionButton @click="createCertification" class="create-button">Create</ActionButton>
        </div>
     
        <BaseContainer class="item-container" :height="'auto'" :maxHeight="'75vh'">
            <BaseTable class="item-table" 
                    :columns="['ID', 'Certification Title', 'Student Number', 'Election Title', 'Date Created', 'Preview / Download']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'69vh'">
                <tr v-for="(certification, index) in certificationsData" :key="index">
                    <td class="my-cell">{{ index + 1 }}</td>
                    <td class="my-cell">{{ certification.Title }}</td>
                    <td class="my-cell">{{ certification.StudentNumber }}</td>
                    <td class="my-cell">{{ certification.ElectionName }}</td>
                    <td class="my-cell">{{ toDate(certification.Date) }}</td>
                    <td class="my-cell">
                        <ActionButton 
                            @click="previewCertification(certification)" class="preview-button mx-2">
                            <i class="fas fa-eye"></i>
                        </ActionButton>
                        <ActionButton 
                            @click="downloadCertification(certification)" class="download-button">
                            <i class="fas fa-download"></i>
                        </ActionButton>
                    </td>
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
            previewCertification(certification){
                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/certification/preview/${certification.CertificationId}`)
                .then((response) => {
                    window.open(response.data.pdf, '_blank');
                })
            },
            downloadCertification(certification){
                axios({
                    url: `${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/certification/download/${certification.CertificationId}`,
                    method: 'GET',
                    responseType: 'blob', // important
                })
                .then((response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    
                    // Use the student number as the filename
                    link.href = url;
                    link.setAttribute('download', `${certification.StudentNumber}.pdf`); // replace with actual student number attribute

                    document.body.appendChild(link);
                    link.click();
                })
            }
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

    .preview-button{
        padding: 2% 8%;
        border-radius: 10px;
        background-color: #38a31b;
    }
    .download-button{
        padding: 2% 8%;
        border-radius: 10px;
        background-color: #136ac2;
    }

    .preview-button:hover{
        background-color: #2e8a14;
    }

    .download-button:hover{
        background-color: #0f4e9c;
    }
</style>