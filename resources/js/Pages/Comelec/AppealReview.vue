<template>
    <title>Appeal Review - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>APPEAL REVIEW</h2>
            </div>
            <div class="col-6">
            </div>      
        </div>   
        
        <div class="row">
            <div class="col-6">
                <BaseContainer :height="'460px'" :maxHeight="'500px'" class="container-left">
                    <div class="form-group row">
                        <div class="col-6">
                            <label class="form-label" for="title">Student Number</label>
                            <input class="form-control" type="title" name="title" v-model="student_number" :disabled="true">
                        </div>
                        <div class="col-6">
                            <label class="form-label" for="title">Student Name</label>
                            <input class="form-control" type="title" name="title" v-model="student_name" :disabled="true">
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="body" class="form-label">Appeal details</label>
                        <textarea class="form-control body" type="text" name="selected-body" v-model="appeal_details" :disabled="true"></textarea>
                    </div>
                    <div class="col-6">
                        <label class="form-label" for="title">Attachment
                            <ToolTip class="mx-2">
                                <slot>
                                    Click the attachment name to view in a new tab.
                                </slot>
                            </ToolTip>
                        </label>
                        <div class="form-control" style="height: 40px !important;"> 
                            <h3 @click.prevent="viewAppeal" 
                                :class="{ 'attachment-clickable': attachment !== 'Loading..', 'attachment-unclickable': attachment === 'Loading..' || attachment === 'No attachment'}">
                                {{ attachment }}
                            </h3>
                        </div>
                    </div>    
                </BaseContainer>
            </div>

            <div class="col-6">
                <BaseContainer :height="'460px'" :maxHeight="'500px'" class="container-right">
                    <div class="row">
                        <div class="form-group col-6">  
                            <label class="form-label" for="title">Appeal Ticket Number</label>
                            <input class="form-control" type="title" name="title" v-model="ticketNumber" :disabled="true">
                        </div>
                        <div class="form-group col-6">  
                            <label class="form-label" for="title">Appeal Status</label>
                            <input class="form-control" :class="{ 'appeal-pending': appeal_status === 'Pending', 'appeal-responded': appeal_status === 'Responded' }" type="title" name="title" v-model="appeal_status" :disabled="true">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="title">Email Subject
                            <ToolTip class="mx-2">
                                <slot>
                                    This will be the subject of the email that will be sent to the student's email.
                                </slot>
                            </ToolTip>
                        </label>
                        <input class="form-control" type="title" name="title" v-model="appeal_subject" :disabled="!selectedItem || appeal_status === 'Responded' || responding">
                    </div>

                    <label for="body2" class="form-label">Response</label>
                    <textarea class="form-control body2" type="text" name="selected-body" v-model="appeal_response" :disabled="!selectedItem || appeal_status === 'Responded' || responding"></textarea>

                    <div class="col-12 save">
                        <ActionButton class="save-btn" @click.prevent="respond" :disabled="responding || appeal_status === 'Responded' || !selectedItem">Respond</ActionButton>
                    </div>
                </BaseContainer>
            </div>
        </div>

        <BaseContainer class="item-container" :height="'auto'" :maxHeight="'75vh'">
            <BaseTable class="item-table"
                    :columns="['ID', 'Student Number', 'Appeal Status', 'Date Submitted']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'69vh'">
                <tr v-for="(appeal, index) in appealsData" :key="index" @click.prevent="selectItem(appeal)"
                    :class="{ 'active-row': selectedItem && selectedItem === appeal }">
                    <td class="my-cell">{{ index + 1 }}</td>
                    <td class="my-cell">{{ appeal.StudentNumber }}</td>
                    <td class="my-cell">{{ appeal.AppealStatus }}</td>
                    <td class="my-cell">{{ toDate(appeal.created_at) }}</td>
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
    import ToolTip from '../../Shared/ToolTip.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup() {
            const selectedItem = ref(null);

            const student_number = ref('');
            const student_name = ref('');
            const appeal_details = ref('');
            const attachment = ref('');
            const attachment_link = ref('');

            const appeal_ticket_number = ref('');
            const appeal_subject = ref('');
            const appeal_status = ref('');
            const appeal_response = ref('');

            const responding = ref(false);

            const fetchAppeals = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election-appeals/all`)
                console.log(`Election appeals successfully fetched. Duration: ${response.duration}`)

                return response.data.appeals;
            };

            const { data: appealsData, isLoading, isSuccess, isError, refetch: appealsDataRefetch } = 
                useQuery({
                    queryKey: ['fetchAppeals'],
                    queryFn: fetchAppeals,
                });

            const selectAppeal = async (selected) => {
                attachment.value = 'Loading..';

                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election-appeals/${selected.ElectionAppealsId}`);
                console.log(`Election appeal successfully fetched. Duration: ${response.duration}`);

                const appeal = response.data.appeal;
                const getFullName = appeal.Student.FirstName + (appeal.Student.MiddleName ? ' ' + appeal.Student.MiddleName : '') + ' ' + appeal.Student.LastName;

                student_number.value = appeal.StudentNumber;
                student_name.value = getFullName;

                appeal_details.value = appeal.AppealDetails;

                if (appeal.AttachmentName) {
                    attachment.value = appeal.AttachmentName;
                }
                else {
                    attachment.value = 'No attachment';
                }

                appeal_ticket_number.value = appeal.ElectionAppealsId;
                appeal_subject.value = appeal.AppealEmailSubject;
                appeal_status.value = appeal.AppealStatus; 
                appeal_response.value = appeal.AppealResponse;
                attachment_link.value = appeal.Attachment;

                return appeal;
            };

            const { data: selectedAppealData,
                    dataUpdatedAt,
                    } =
                useQuery({
                    queryKey: [`selectAppeal-${selectedItem.ElectionAppealsId}`],
                    queryFn: () => selectAppeal,
                });

            return {
                selectedItem,

                appealsData,
                appealsDataRefetch,
                isLoading,
                isSuccess,
                isError,

                selectAppeal,
                selectedAppealData,
                dataUpdatedAt,

                student_number,
                student_name,
                appeal_details,
                attachment,
                attachment_link,
                
                appeal_ticket_number,
                appeal_subject,
                appeal_status,
                appeal_response,

                responding,
            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            BaseContainer,
            BaseTable,
            ImageSkeleton,
            ToolTip,
        },
        computed: {
            ticketNumber() {
                if (!this.appeal_ticket_number) {
                    return '';
                }

                return '#' + this.appeal_ticket_number;
            }
        },
        methods: {
            toDate(date){
                return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            },
            selectItem(appeal){
                if (this.responding) {
                    return;
                }

                this.selectedItem = appeal;
                this.selectAppeal(appeal);
            },
            viewAppeal() {
                const appeal = this.selectedItem;
                if (!appeal || !this.attachment || this.attachment === 'Loading..' || this.attachment === 'No attachment') {
                    return;
                }
                
                const attachment_url = this.attachment_link;
                window.open(attachment_url, '_blank')
            },
            validateInputs() {
                if (!this.appeal_subject) {
                    alert('Please enter an email subject.');
                    return false;
                }
                if (!this.appeal_response) {
                    alert('Please enter a response.');
                    return false;
                }

                return true;
            },
            respond() {
                if (!this.validateInputs()) {
                    return;
                }
                if (this.responding || this.appeal_status === 'Responded') {
                    return;
                }

                this.responding = true;

                const appeal = this.selectedItem;
                const data = {
                    id: appeal.ElectionAppealsId,
                    subject: this.appeal_subject,
                    response: this.appeal_response,
                };

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election-appeals/respond`, data)
                    .then((response) => {
                        console.log(`Election appeal successfully responded. Duration: ${response.duration}`);
                        alert('Election appeal successfully responded.');

                        this.appeal_status = 'Responded';
                    })
                    .catch((error) => {
                        console.log(error);
                        alert('An error has occured.');
                    })
                    .finally(() => {
                        this.responding = false;
                    });
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

    .components h2{
        font-weight: 800;
        font-size: 30px;
        margin-bottom: 1.5%;
    }

    .form-control, .form-select, .body {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .item-container{
        margin-bottom: 2%;
    }

    .body{
        resize: none;
        overflow-y: auto;
        height: 200px;
    }

    .body2{
        resize: none;
        overflow-y: auto;
        height: 160px;
    }

    .form-group{
        padding-bottom: 15px;
    }

    .save{
        text-align: right;
    }

    .save-btn{
        margin-top: 13px;
    }

    .container-left {
        margin-right: 3px;
    }   

    .container-right {
        margin-left: 3px;
    }

    .attachment-clickable{
        font-size: 16px;
        margin-top: 1%;
        width: fit-content;
    }

    .attachment-clickable:hover{
        cursor: pointer;
        text-decoration: underline;
    }

    .attachment-unclickable{
        font-size: 16px;
        margin-top: 1%;
        color: #B90321;
        width: fit-content;
        text-decoration: none !important;
        cursor: default !important;
    }

    .appeal-pending{
        color: black;
    }
    .appeal-responded{
        color: #4fbf4b;
    }
</style>