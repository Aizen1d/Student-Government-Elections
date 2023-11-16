<template>
    <title>Approvals View Party - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row utilities">
            <div class="col-6">
                <h2 class="my-1">
                    <span class="return" @click="returnPage">Approvals</span> > View > Partylist
                </h2>
            </div>
            <template v-if="!isPartylistLoading">
                <div v-if="party_list_status === 'Pending'" class="col-6" style="text-align: end;">
                    <ActionButton @click.prevent="acceptPartylist" class="accept-button" style="margin-right: 2% !important; background-color: rgb(71, 182, 43);">Approve</ActionButton>
                    <ActionButton @click.prevent="rejectPartylist" class="my-2">Reject</ActionButton>
                </div>

                <div v-else-if="party_list_status !== 'Pending'" class="col-6" style="text-align: end;">
                    <h1 v-if="party_list_status === 'Approved'" style="font-weight: 800; font-size: 2rem; color: rgb(71, 182, 43);">Approved</h1>
                    <h1 v-else-if="party_list_status === 'Rejected'" style="font-weight: 800; font-size: 2rem; color: #B90321">Rejected</h1>
                </div>
            </template>
        </div>

        <div v-if="isPartylistLoading">
            <div class="row">
                <div class="col-6">
                    <div class="note-timeline">
                        <h6 class="mx-3">Basic Information</h6>
                    </div>
                    <ImageSkeleton v-if="isPartylistLoading" 
                            :loading="isPartylistLoading" 
                            :itemCount="1" 
                            :borderRadius="'0px'"
                            :imageWidth="'38vw'" 
                            :imageHeight="'60vh'"
                            :containerMargin="'0% -0%'"
                            :itemMargin="'0em'">
                    </ImageSkeleton>

                </div>

                <div class="col-6">
                    <div class="note-timeline">
                        <h6 class="mx-3">Attachments</h6>
                    </div>
                    <ImageSkeleton v-if="isPartylistLoading" 
                            :loading="isPartylistLoading" 
                            :itemCount="1" 
                            :borderRadius="'0px'"
                            :imageWidth="'38vw'" 
                            :imageHeight="'60vh'"
                            :containerMargin="'0% -0%'"
                            :itemMargin="'0em'">
                    </ImageSkeleton>
                    
                </div>
            </div>
        </div>

        <div v-if="!isPartylistLoading">
            <div class="row">
                <div class="col-6">
                    <div class="note-timeline">
                        <h6 class="mx-3">Basic Information</h6>
                    </div>
                    <div class="box">
                        <div class="first-info">
                            <label class="form-label" for="name">Party Name</label>
                            <input class="form-control" type="text" name="name" v-model="partylistData.PartyListName" :disabled="true">
                        </div>

                        <div class="margin">
                            <label class="form-label" for="type">Email Address</label>
                            <input class="form-control" type="text" name="name" v-model="partylistData.EmailAddress" :disabled="true">
                        </div>

                        <div class="margin">
                            <label class="form-label" for="type">Cellphone Number</label>
                            <input class="form-control" type="text" name="name" v-model="partylistData.CellphoneNumber" :disabled="true">
                        </div>

                        <div class="margin">
                            <label for="desc" class="form-label">Description</label>
                            <textarea class="form-control text-area-input" type="text" name="desc" v-model="partylistData.Description" :disabled="true"></textarea>
                        </div>

                        <div class="margin">
                            <label for="desc" class="form-label">Mission</label>
                            <textarea class="form-control text-area-input" type="text" name="desc" v-model="partylistData.Mission" :disabled="true"></textarea>
                        </div>

                        <div class="margin">
                            <label for="desc" class="form-label">Vision</label>
                            <textarea class="form-control text-area-input" type="text" name="desc" v-model="partylistData.Vision" :disabled="true"></textarea>
                        </div>

                        <div class="margin">
                            <label for="desc" class="form-label">Platforms</label>
                            <textarea class="form-control text-area-input" type="text" name="desc" v-model="partylistData.Platforms" :disabled="true"></textarea>
                        </div>
                    </div>
                </div>

                <div class="col-6">
                    <div class="note-timeline">
                        <h6 class="mx-3">Attachments</h6>
                    </div>
                    <div class="box">
                        <h6 class="first-info">Image Attachment</h6>

                        <div class="image">
                            <h3 v-if="!partylistData.ImageAttachment || partylistData.ImageAttachment === '' ">No image attached</h3>
                            <img v-else :src="partylistData.ImageAttachment" @click="viewImage(partylistData.ImageAttachment)" style="width: 80%; height: 50%; margin-left: 0%; margin-top: 1%; cursor: pointer;" >
                        </div>

                        <hr class="my-4">
                        <h6 class="">Video Attachment</h6>

                        <div v-if="!partylistData.VideoAttachment || partylistData.VideoAttachment === '' " style="text-align: center;">
                            <h3>No video attached</h3>
                        </div>
                        <iframe v-else style="margin-left: 10%; margin-top: 1%; margin-bottom: 1%;" width="80%" height="350px" :src="getEmbedUrl(partylistData.VideoAttachment)" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                    </div>

                </div>
            </div>
        </div>

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

    import { useQuery, useMutation, useQueryClient  } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup(props) {
            const type = ref(props.type);
            const id = ref(Number(props.id));

            const party_list_status = ref('');

            const fetchPartylistData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/${id.value}`);
                console.log(`Partylist with id ${id.value} fetched successfully. Duration: ${response.duration}`)

                return response.data.partylist;
            }

            const { data: partylistData,
                    isLoading: isPartylistLoading,
                    isError: isPartylistError,
                    error: partylistError,} = 
                    useQuery({
                        queryKey: [`fetchPartylistData-${id.value}`],
                        queryFn: fetchPartylistData,
                    })

            watchEffect(() => {
                if (!isPartylistLoading.value) {
                    party_list_status.value = partylistData.value.Status;
                }
            })

            return {
                type,
                id,
                party_list_status,

                partylistData,
                isPartylistLoading,
                isPartylistError,
                partylistError,
            }
        },
        components: { Navbar, Sidebar, ActionButton, BaseContainer, BaseTable, ActionButton, ImageSkeleton },
        props: {
            type: '',
            id: '',
        },
        methods: {
            returnPage() {
                router.visit('/comelec/approvals');
            },
            formatDate(date) {
                let options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(date).toLocaleDateString(undefined, options);
            },
            viewImage(image) {
                window.open(image, '_blank');
            },
            getEmbedUrl(url) {
                let videoId = url.split('v=')[1];
                
                return 'https://www.youtube.com/embed/' + videoId;
            },
            acceptPartylist() {
                const confirm = window.confirm('Are you sure you want to accept this Partylist?');
                if (!confirm) return;

                axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/${this.id}/accept`)
                    .then((response) => {
                        console.log(response);

                        this.party_list_status = 'Approved';
                    })
                    .catch((error) => {
                        console.log(error);
                    })
            },
            rejectPartylist() {
                const confirm = window.confirm('Are you sure you want to reject this Partylist?');
                if (!confirm) return;

                axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/${this.id}/reject`)
                    .then((response) => {
                        console.log(response);

                        this.party_list_status = 'Rejected';
                    })
                    .catch((error) => {
                        console.log(error);
                    })
            },
        },
    }
</script>

<style scoped>
    .utilities{
        margin-bottom: 1%;
    }

    .accept-button:disabled{
        background-color: #cccccc !important;
    }

    .return{
        color: #B90321;
        cursor: pointer;
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
    
    .form-control, .form-select {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .margin{
        margin-right: -1%;
        margin-left: -1%;
    }

    .button{
        margin-top: 5%;
    }

    .save{
        text-align: end;
    }

    .note{
        margin-top: 1.5%;
        background-color: #c2eba7;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 2%;
    }

    .note h6{
        margin-top: 10px;
    }

    .note-timeline{
        margin-top: 1.5%;
        background-color: #eec865;
        padding: 1.5%;
    }

    .note-timeline h6{
        margin-top: 10px;
    }

    .box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 4.5%;
        margin-bottom: 3%;
    }

    .upper-box{
        padding-bottom: 5%;
    }

    .position-box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 3% 3% 2% 3%;
    }

    .first-info{
        margin-top: -2%;
    }

    .text-area-input{
        height: fit-content;
        resize: none;
    }

    .margin{
        margin-top: 3%;
        margin-left: 0%;
    }

    .list{
        margin-top: 3.5%;
    }

    .head{
        text-align: center;
    }

    .position-btn{
        text-align: end;
    }

    .election-btn{
        text-align: end;
    }

    .new-btn{
        margin-top: .5%;
    }

    .remove-btn {
        margin-left: -1%;
        margin-top: -10%;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
    }

    .remove-btn:hover{
        color: #B90321;
    }

    .remove-btn:disabled{
        color: #cccccc;
    }

    .reusable-btn {
        margin-top: -10% !important;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #00ae0c;
    }

    .reusable-btn:hover{
        color: rgb(12, 194, 2);
    }

    .reusable-btn:disabled{
        color: #cccccc !important;
    }

    .cancel{
        color: black;
        background-color: #FDD5D5;
        margin-right: 2%;
    }

    .cancel:hover{
        background-color: #ffcfcf;
    }

    .image{
        text-align: center;
    }

    .pic{
        width: 155px;
        height: 155px;
        object-fit: cover;
        border-radius: 100px;
        outline: 1px solid #bbbb;
        cursor: pointer;
    }
</style>