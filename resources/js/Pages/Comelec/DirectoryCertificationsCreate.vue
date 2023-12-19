<template>
    <title>Directory - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h2 class="my-1">
                <span class="return" @click="returnDirectory">Directory</span> > <span class="return" @click="returnCertifications">Certifications</span> > Create
            </h2>
        </div>

        <form action="">
            <div class="mainbox">
                <div class="form-group">
                    <label class="form-label" for="title">Certification Title</label>
                    <input class="form-control" type="text" name="title" v-model="title_input">
                </div>

                <div class="form-group">
                    <label class="form-label" for="date">Election Name</label>
                    <select class="form-select margin" name="SY" v-model="election_input">
                        <option value="" disabled hidden selected>Select election</option>
                        <option v-for="(election, index) in electionsData" :key="index" :value="election.id">
                            {{ election.title }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="date">Date</label>
                    <input class="form-control" type="date" name="date" v-model="date_input">
                </div>

                <div class="form-group">
                    <label class="form-label" for="date">Admin Signatory Quantity</label>
                    <select class="form-select margin" name="SY" v-model="signatory_input">
                        <option value="0" disabled hidden selected>Select quantity</option>
                        <option v-for="number in 4" :key="number" :value="number">
                            {{ number }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="signatories" v-for="(signatory, index) in signatories" :key="index">                    
                <div class="form-group">
                    <label class="form-label" for="signatory-name">Signatory Name</label>
                    <input class="form-control" type="text" name="signatory-name" v-model="signatory.name">
                </div>

                <div class="form-group">
                    <label class="form-label" for="signatory-position">Signatory Position</label>
                    <input class="form-control" type="text" name="signatory-position" v-model="signatory.position">
                </div>
            </div>

            <div class="buttons">
                <button class="cancel-button" @click.prevent="cancel" :disabled="creating">Cancel</button>
                <ActionButton class="create-button" @click.prevent="createCertification" :disabled="creating">Create</ActionButton>
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
    import ImageSkeleton from '../../Skeletons/ImageSkeleton.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup() {
            const title_input = ref('');
            const election_input = ref('');
            const date_input = ref('');
            const signatory_input = ref(0);

            const signatories = ref([]);

            const creating = ref(false);

            watch(signatory_input, (newVal, oldVal) => {
                if (newVal > oldVal) {
                    for (let i = 0; i < newVal - oldVal; i++) {
                        signatories.value.push({ name: '', position: '' });
                    }
                } 
                else {
                    signatories.value = signatories.value.slice(0, newVal);
                }
            });

            const fetchElectionsTable = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`);
                console.log(`Elections table fetched successfully. Duration: ${response.duration}`)

                const now = new Date();
                const elections = response.data.elections
                    .filter(item => new Date(item.VotingEnd) < now)
                    .map(item => {
                        return {
                            id: item.ElectionId,
                            title: item.ElectionName,
                            organization: item.ElectionType,
                            voting_end: item.VotingEnd,
                        }
                    });

                return elections;
            }

            const { data: electionsData, isLoading, isSuccess, isError, dataUpdatedAt } = 
                useQuery({
                    queryKey: ['fetchElections'],
                    queryFn: fetchElectionsTable,
                });

            return {
                title_input,
                election_input,
                date_input,
                signatory_input,
                signatories,
                creating,

                electionsData,
                isLoading,
                isSuccess,
                isError,
                dataUpdatedAt,
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
            returnDirectory() {
                if (this.creating) {
                    return
                }

                router.visit('/comelec/directory');
            },
            returnCertifications() {
                if (this.creating) {
                    return
                }

                router.visit('/comelec/directory/certifications');
            },
            cancel() {
                if (this.creating) {
                    return
                }
                
                router.visit('/comelec/directory/certifications');
            },
            validateInputs() {
                if (this.title_input === '') {
                    alert('Title is required.');
                    return false;
                }
                if (this.election_input === '') {
                    alert('Election is required.');
                    return false;
                }
                if (this.date_input === '') {
                    alert('Date is required.');
                    return false;
                }
                if (this.signatory_input === 0) {
                    alert('Signatory quantity is required.');
                    return false;
                }

                // Validate signatories
                for (let i = 0; i < this.signatories.length; i++) {
                    if (this.signatories[i].name === '') {
                        alert('Signatory name is required.');
                        return false;
                    }
                    if (this.signatories[i].position === '') {
                        alert('Signatory position is required.');
                        return false;
                    }
                }

                return true;
            },
            createCertification() {
                if (this.validateInputs()) {
                    // Send data to backend
                    const data = {
                        title: this.title_input,
                        election_id: Number(this.election_input),
                        date: this.date_input,
                        quantity: String(this.signatory_input),
                        signatories: this.signatories,
                    }

                    this.creating = true;

                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/certification/create`, data)
                        .then(response => {
                            console.log(response);

                            alert('Certification created successfully.');
                            
                            // Open the PDF in a new tab
                            if (response.data.pdf_url) {
                                window.open(response.data.pdf_url);
                            }

                            router.visit('/comelec/directory/certifications');
                        })
                        .catch(error => {
                            console.log(error);

                            alert('An error occurred. Please try again.');
                        })
                        .finally(() => {
                            this.creating = false;
                        });
                }
            }
        }
    }
</script>

<style scoped>
    /*!!!START OF CSS!!!*/

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

    .mainbox, .list, .signatories, .buttons{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1%;
        padding: 30px 30px 20px 30px;
        border-radius: 7px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        width: 50%;
    }

    .body{
        height: 200px;
    }

    .form-group{
        padding-bottom: 15px;
    }

    .buttons{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .cancel-button{
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 15px 20px 15px 20px;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
    }

    .create-button:disabled{
        background-color: #cccccc;
    }
</style>