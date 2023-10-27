<template>
    <Navbar></Navbar>

    <div class="main">
        <div class="header row">
            <div class="col">
                <h1>
                    <span class="return" @click="returnPage">{{ electionName }}</span>&nbsp;>&nbsp;File Certificate of Candidacy
                </h1>
            </div>
        </div>

        <form action="">
            <div class="row coc g-5">
                <div class="col-7">
                    <div class="info">
                        <div class="row marg">
                            <label for="per-info" class="col-4 col-form-label">Applicant Information</label>
                            <div class="col-6 box">
                                <label class="form-label">Student Number</label>
                                <input type="text" class="form-control margin" v-model="student_number">

                                <label class="form-label">Verification Code</label>
                                <input type="text" class="form-control margin" v-model="verification_code">

                                <label class="form-label">Address</label>
                                <input type="text" class="form-control margin" v-model="address">
                            </div>
                        </div>
    
                        <hr class="my-2">

                        <div class="row">
                            <label for="per-info" class="col-4 col-form-label">Election Information</label>
                            <div class="col-6 box">
                                <label class="form-label">Political Affiliation</label>

                                <select class="form-select margin" aria-label="Default select example" v-model="political_affiliation">
                                    <option value="" hidden selected>Select</option>
                                    <option value="Independent">Independent</option>
                                    <option value="Party List">Party List</option>
                                </select>

                                <div v-if="political_affiliation !== '' && political_affiliation !== 'Independent'">
                                    <label class="form-label">Select Party List</label>
                                    <select class="form-select margin" aria-label="Default select example" v-model="party_list">
                                        <option value="" hidden selected>Select</option>
                                    </select>
                                </div>

                                <div v-if="political_affiliation !== ''">
                                    <label class="form-label">Select Position</label>
                                    <select class="form-select margin" aria-label="Default select example" v-model="selected_position">
                                        <option value="" hidden selected>Select</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="col-5">
                    <div class="attachments">
                        <h6>Display Photo</h6>

                        <div class="image">
                            <img :src="store.display_photo" alt="" class="pic" draggable="false">
                        </div>

                        <div class="row marge">
                            <div class="col-4">
                                <label for="file-upload" class="mx-3 display-photo-file-upload">
                                    Select File
                                </label>
                                <input id="file-upload" type="file" style="display: none;" @change="handleDisplayPhotoFile">
                            </div>
                            <div class="col-8">
                                <label class="mx-3 text-truncate" style="max-width: 100%;">
                                    {{ display_photo_file_name }}
                                </label>
                            </div>
                        </div>

                        <hr class="my-3">
                        <h6>Certification of Grades</h6>

                        <div v-if="store.certification_of_grades !== '' ">
                            <img :src="store.certification_of_grades" alt="Certification of Grades" style="width: 500px; height: 300px; margin-left: 11.5%; margin-top: 1%;" >
                            <input id="file-upload" type="file" style="display: none;" @change="handleCertificationFile">
                        </div>
                        
                        <div class="row my-4">
                            <div class="col-4">
                                <label for="file-upload" class="mx-3 grades-file-upload">
                                    Select File
                                </label>
                            </div>
                            <div class="col-8">
                                <label class="mx-3 my-2 text-truncate" style="max-width: 100%;">
                                    {{ certification_of_grades_file_name }}
                                </label>
                            </div>
                        </div>

                    </div>
                    <div class="btns">
                        <ActionButton class="mx-4" @click.prevent="returnPage">Cancel</ActionButton>
                        <ActionButton>Verify</ActionButton>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'
    import ActionButton from '../Shared/ActionButton.vue'
    import { useCoCDraftStore } from '../Stores/CoCDraftStore'

    import { ref, watchEffect, watch, computed } from 'vue'
    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    
    export default {
        setup(props) {
            const store = useCoCDraftStore();

            const id = ref(Number(props.id))
            const electionName = ref(props.electionName)

            const student_number = ref(store.student_number)
            const verification_code = ref(store.verification_code)
            const address = ref(store.address)
            const political_affiliation = ref(store.political_affiliation)
            const party_list = ref(store.party_list)
            const selected_position = ref(store.selected_position)

            const display_photo = ref(store.display_photo)
            const display_photo_file_name = ref(store.display_photo_file_name)

            const certification_of_grades = ref(store.certification_of_grades)
            const certification_of_grades_file_name = ref(store.certification_of_grades_file_name)

            watch(student_number, (newValue, oldValue) => {
                store.student_number = newValue
            })

            watch(verification_code, (newValue, oldValue) => {
                store.verification_code = newValue
            })

            watch(address, (newValue, oldValue) => {
                store.address = newValue
            })

            watch(political_affiliation, (newValue, oldValue) => {
                store.political_affiliation = newValue
            })

            watch(party_list, (newValue, oldValue) => {
                store.party_list = newValue
            })

            watch(selected_position, (newValue, oldValue) => {
                store.selected_position = newValue
            })

            watch(display_photo, (newValue, oldValue) => {
                if (newValue) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        store.display_photo = reader.result;
                        store.display_photo_file_name = display_photo_file_name.value;
                    };
                    reader.readAsDataURL(newValue);
                }
            });

            watch(certification_of_grades, (newValue, oldValue) => {
                if (newValue) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        store.certification_of_grades = reader.result;
                        store.certification_of_grades_file_name = certification_of_grades_file_name.value;
                    };
                    reader.readAsDataURL(newValue);
                }
            });

            const handleDisplayPhotoFile = (event) => {
                const file = event.target.files[0];

                display_photo_file_name.value = file.name;
                display_photo.value = file;
            };

            const handleCertificationFile = (event) => {
                const file = event.target.files[0];

                certification_of_grades_file_name.value = file.name;
                certification_of_grades.value = file;
            };

            return {
                store,
                id,
                electionName,
                student_number,
                verification_code,
                address,
                political_affiliation,
                party_list,
                selected_position,
                display_photo,
                display_photo_file_name,
                certification_of_grades,
                certification_of_grades_file_name,

                handleDisplayPhotoFile,
                handleCertificationFile
            }
        },
        components:{
            Standards,
            Navbar,
            ActionButton,
        },
        props:{
            id: '',
            electionName: '',
        },
        methods:{
            returnPage(){
                router.visit(`/elections/view?id=${this.id}`)
            },
        },
    }
</script>

<style scoped>
    .text-truncate {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
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
    .main{
        margin: 3% 5%;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .header{
        margin-top: -.5%;
        margin-bottom: 2%;
    }

    .header h1{
        font-size: 28px;
        font-weight: 800;
        height: 100%;
    }

    .btns{
        text-align: end;
        margin-top: 3%;
    }

    .draft-button{
        text-align: end;
    }

    .display-photo-file-upload {
        margin-top: 5%;
        margin-bottom: 10%;
        padding: 7px;
        width: 100%;
        font-size: 100%;
        border: 1px solid #ccc;
        border-radius: 8px;
        display: inline-block;
        cursor: pointer;
        text-align: center;
    }

    .grades-file-upload {
        padding: 7px;
        width: 100%;
        font-size: 100%;
        border: 1px solid #ccc;
        border-radius: 8px;
        display: inline-block;
        cursor: pointer;
        text-align: center;
    }

    .coc{
        font-family: 'Source Sans Pro', sans-serif;
    }

    .info, .attachments{
        background-color: #F5F8F9;
        padding: 2%;
        border-radius: 10px;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    }

    .attachments{
        background-color: #F5F8F9;
        padding: 3%;
        border-radius: 10px;
    }

    .attachments h6{
        font-weight: bold;
        font-size: 17px;
    }

    .form-label{
        margin: 1% 0%;
    }

    .a{
        margin: 1.5% 0%;
    }

    .col-form-label{
        font-weight: bold;
        font-size: 17px;
    }

    .box{
        margin-top: 0.5%;
    }

    .margin{
        margin-bottom: 2%;
        margin-left: 0%;
    }

    .marg{
        margin-top: -1%;
    }

    .marge{
        margin: 1% 0%;
        margin-top: 2%;
        display: flex;
        align-items: center;
        width: 100%;
    }

    .pic{
        width: 155px;
        height: 155px;
        object-fit: cover;
        border-radius: 100px;
        outline: 1px solid #bbbb;
    }

    .image{
        text-align: center;
    }

    .s{
        padding: 0%;
    }
</style>