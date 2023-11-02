<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row utilities">
            <div class="col-6">
                <h2 class="my-1" v-if="!isLoading">
                    <span class="return" @click="returnPage">Elections</span> > View > {{ election_name_input  }}
                </h2>
            </div>
            <div class="col-6" style="text-align: end;">
                <ActionButton @click="deleteElection" class="new-btn">Delete Election</ActionButton>
            </div>     
        </div>

        <form @submit.prevent="submit">
            <div class="row g-4">
                <div class="col-6">
                    <div class="note">
                        <h6>Election name and type.</h6>
                    </div>
                    <div class="box upper-box">
                        <label class="form-label" for="name">Election Name</label>
                        <input class="form-control margin" type="text" name="name" v-model="election_name_input" :disabled="true">
                        
                        <label class="form-label" for="type">Election Type</label>
                        <input class="form-control margin" type="text" name="name" v-model="election_type_input" :disabled="true">
                    </div>
                </div>
                <div class="col-6">
                    <div class="note">
                        <h6>The current school year and semester for this election.</h6>
                    </div>
                    <div class="box upper-box">
                        <label class="form-label" for="sy">School Year</label>
                        <input type="text" class="form-control margin" v-model="election_school_year_input" :disabled="true">
    
                        <label class="form-label" for="sem">Semester</label>
                        <select class="form-control" name="sem" v-model="election_semester_input" :disabled="true">
                            <option value="" disabled hidden selected>Select semester</option>
                            <option value="1st Semester">1st Semester</option>
                            <option value="2nd Semester">2nd Semester</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div>
                <div class="note-timeline">
                    <h6>Timeline for the whole election.</h6>
                </div>
                <div class="box">
                    <div class="row">
                        <label for="election-period" class="col-3 col-form-label">Election Period</label>
                        <div class="col-5">
                            <label class="form-label" for="e-start">Election Start</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_start_input" :disabled="true">

                            <label class="form-label" for="e-end">Election End</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_end_input" :disabled="true">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Filing of COC Period</label>
                        <div class="col-5">
                            <label class="form-label" for="f-start">Filing Start</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_filing_coc_start_input" :disabled="true">

                            <label class="form-label" for="f-end">Filing End</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_filing_coc_end_input" :disabled="true">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Campaign Period</label>
                        <div class="col-5">
                            <label class="form-label" for="c-start">Campaign Start</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_campaign_start_input" :disabled="true">

                            <label class="form-label" for="c-end">Campaign End</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_campaign_end_input" :disabled="true">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Voting Period</label>
                        <div class="col-5">
                            <label class="form-label" for="v-start">Voting Start</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_voting_start_input" :disabled="true">

                            <label class="form-label" for="v-end">Voting End</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_voting_end_input" :disabled="true"> 
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Appeal Period</label>
                        <div class="col-5">
                            <label class="form-label" for="a-start">Appeal Start</label>
                            <input type="datetime-local" class="form-control margin" v-model="election_appeal_start_input" :disabled="true">

                            <label class="form-label" for="a-end">Appeal End</label>
                            <input type="datetime-local" class="form-control" v-model="election_appeal_end_input" :disabled="true">
                        </div>
                    </div>
                </div>
            </div>

            <div>
                <div class="note-timeline">
                    <div class="row">
                        <div class="col-6 my-1">
                            <h6>Positions for this election.</h6>
                        </div>
                    </div>
                </div>
                <div class="position-box mb-4" v-for="(position, index) in position_list" :key="index">
                    <div class="row g-4">
                        <div class="col">
                            <label class="form-label" for="position-name">Position Name</label>
                            <div class="row">
                                <div class="col-3">
                                    <input type="text" class="form-control position-name margin" 
                                        v-model="position.name" 
                                        :disabled="true">
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-3">
                                    <label class="form-label" for="position-quantity">Position Quantity</label>
                                    <input type="number" min="1" class="form-control position-quantity margin" v-model.number="position.quantity" :disabled="true">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
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

    import { useQuery, useMutation, useQueryClient  } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup(props) {
            const election_id = props.id;

            let election_name_input = ref('');
            let election_type_input = ref('');
            let election_school_year_input = ref('');
            let election_semester_input = ref('');
            let election_start_input = ref('');
            let election_end_input = ref('');
            let election_filing_coc_start_input = ref('');
            let election_filing_coc_end_input = ref('');
            let election_campaign_start_input = ref('');
            let election_campaign_end_input = ref('');
            let election_voting_start_input = ref('');
            let election_voting_end_input = ref('');
            let election_appeal_start_input = ref('');
            let election_appeal_end_input = ref('');

            const position_count = ref(1);
            const position_list = ref([]); // The list of positions for this election

            const fetchElectionData = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${election_id}`)

                return response.data
            }

            const { data, isLoading, isSuccess, isError, dataUpdatedAt } = 
                useQuery({
                    queryKey: [`fetchElectionData-${election_id}`],
                    queryFn: fetchElectionData,
                });

            watchEffect(() => {
                if (isSuccess && data.value) {
                    election_name_input.value = data.value.election.ElectionName;
                    election_type_input.value = data.value.election.ElectionType;
                    election_school_year_input.value = data.value.election.SchoolYear;
                    election_semester_input.value = data.value.election.Semester;
                    election_start_input.value = data.value.election.ElectionStart;
                    election_end_input.value = data.value.election.ElectionEnd;
                    election_filing_coc_start_input.value = data.value.election.CoCFilingStart;
                    election_filing_coc_end_input.value = data.value.election.CoCFilingEnd;
                    election_campaign_start_input.value = data.value.election.CampaignStart;
                    election_campaign_end_input.value = data.value.election.CampaignEnd;
                    election_voting_start_input.value = data.value.election.VotingStart;
                    election_voting_end_input.value = data.value.election.VotingEnd;
                    election_appeal_start_input.value = data.value.election.AppealStart;
                    election_appeal_end_input.value = data.value.election.AppealEnd;
                    
                    position_list.value = data.value.positions.map((item) => {
                        return {
                            count: position_count.value++,
                            name: item.PositionName,
                            value: item.PositionName,
                            quantity: item.PositionQuantity,
                        }
                    });
                }
            })

            return {
                election_name_input,
                election_type_input,
                election_school_year_input,
                election_semester_input,
                election_start_input,
                election_end_input,
                election_filing_coc_start_input,
                election_filing_coc_end_input,
                election_campaign_start_input,
                election_campaign_end_input,
                election_voting_start_input,
                election_voting_end_input,
                election_appeal_start_input,
                election_appeal_end_input,
                position_count,
                position_list,
                election_id,

                isLoading,
                isSuccess
            }
        },
        components: { Navbar, Sidebar, ActionButton, BaseContainer, BaseTable },
        props: {
            id: '',
        },
        methods: {
            returnPage() {
                router.visit('/comelec/elections');
            },
            deleteElection() {
                const confirmDelete = confirm('Are you sure you want to delete this election?');

                if (!confirmDelete) {
                    return;
                }

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/delete`, {
                    id: this.election_id,
                })
                .then((response) => {
                    console.log(`Election deleted successfully. Duration: ${response.duration}`);

                    alert(response.data.message)
                    router.visit('/comelec/elections');
                })
                .catch((error) => {
                    console.log(error);
                });
            }
        },
    }
</script>

<style scoped>
    .utilities{
        margin-bottom: 1%;
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
        background-color: #eec865;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 2%;
    }

    .note h6{
        margin-top: 10px;
    }

    .note-timeline{
        margin-top: 1.5%;
        background-color: #eec865;
        padding: 1.1%;
    }

    .note-timeline h6{
        margin-top: 10px;
    }

    .box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        width: 100%;
        height: 72%;
        padding: 3%;
    }

    .upper-box{
        padding-bottom: 5%;
    }

    .position-box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 3% 3% 2% 3%;
    }

    .margin{
        margin-bottom: 2%;
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
</style>