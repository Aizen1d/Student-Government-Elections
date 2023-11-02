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
                                <input type="text" class="form-control margin" maxlength="15" placeholder="Enter your student number" :disabled="is_submitting" v-model="student_number">

                                <label class="form-label">Verification Code</label>
                                <div style="display: flex;">
                                    <input type="text" class="form-control margin" placeholder="Enter your verification code" :disabled="is_submitting" v-model="verification_code">
                                    <ActionButton @click.prevent="sendCode" :disabled="isSending || isSent || is_submitting" 
                                                        :style="{ width: isSent ? '20em' : '15em' }"
                                                        style="font-size: 1em;
                                                        margin-left: 5%;
                                                        height: 2.2em; 
                                                        padding: 0px 0px 0px 0px !important;">{{ buttonText }}</ActionButton>
                                </div>

                                <label class="form-label">Address</label>
                                <input type="text" class="form-control margin" placeholder="Enter your address" :disabled="is_submitting" v-model="address">
                            </div>
                        </div>
    
                        <hr class="my-2">

                        <div class="row">
                            <label for="per-info" class="col-4 col-form-label">Election Information</label>
                            <div class="col-6 box">
                                <label class="form-label">Political Affiliation</label>

                                <select class="form-select margin" aria-label="Default select example" :disabled="is_submitting" v-model="political_affiliation">
                                    <option value="" hidden selected>Select</option>
                                    <option value="Independent">Independent</option>
                                    <option value="Party List">Party List</option>
                                </select>

                                <div v-if="political_affiliation !== '' && political_affiliation !== 'Independent'">
                                    <label class="form-label">Select Party List</label>
                                    <select class="form-select margin" aria-label="Default select example" :disabled="is_submitting" v-model="party_list">
                                        <option value="" hidden selected>Select</option>
                                    </select>
                                </div>

                                <div v-if="political_affiliation !== ''">
                                    <label class="form-label">Select Position</label>
                                    <select class="form-select margin" aria-label="Default select example" :disabled="is_submitting" v-model="selected_position">
                                        <option value="" hidden selected>Select</option>
                                        <option v-for="(position, index) in positionsData" :key="index" :value="position.PositionName">{{ position.PositionName }}</option>
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
                            <img v-if="display_photo_base_64" :src="display_photo_base_64" alt="" class="pic" draggable="false">
                            <img v-else src="../../images/dog_placeholder.jpg" alt="" class="pic" draggable="false">
                        </div>

                        <div class="row marge">
                            <div class="col-4">
                                <label for="display-file-upload" class="mx-1 display-photo-file-upload">
                                    Select File
                                </label>
                                <input id="display-file-upload" type="file" accept="image/*" style="display: none;" :disabled="is_submitting" @change="handleDisplayPhotoFile">
                            </div>
                            <div class="col-8">
                                <label class="mx-3 text-truncate" style="max-width: 100%;">
                                    {{ display_photo_file_name }}
                                </label>
                            </div>
                        </div>

                        <hr class="my-3">
                        <h6>Certification of Grades</h6>

                        <div v-if="certification_of_grades_base_64">
                            <img :src="certification_of_grades_base_64" alt="Certification of Grades" style="width: 500px; height: 300px; margin-left: 11.5%; margin-top: 1%;" >
                        </div>
                        
                        <div class="row my-4">
                            <div class="col-4">
                                <label for="grades-file-upload" class="mx-3 grades-file-upload">
                                    Select File
                                </label>
                                <input id="grades-file-upload" type="file" accept="image/*" style="display: none;" :disabled="is_submitting" @change="handleCertificationFile">
                            </div>
                            <div class="col-8">
                                <label class="mx-3 my-2 text-truncate" style="max-width: 100%;">
                                    {{ certification_of_grades_file_name }}
                                </label>
                            </div>
                        </div>

                    </div>
                    <div class="btns">
                        <ActionButton :disabled="is_submitting" class="mx-4" @click.prevent="returnPage">Cancel</ActionButton>
                        <ActionButton :disabled="is_submitting" @click.prevent="submit">{{ submitStatus }}</ActionButton>
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

    import { ref, watchEffect, watch, computed } from 'vue'
    import { useQuery } from "@tanstack/vue-query";
    import { router } from '@inertiajs/vue3';
    import { useLocalStorage } from '@vueuse/core';
    import axios from 'axios'

    export default {
        setup(props) {
            const id = ref(Number(props.id))
            const electionName = ref(props.electionName)

            const student_number = useLocalStorage(`coc_student_number_${id.value}`, '')

            const verification_code = useLocalStorage(`coc_verification_code_${id.value}`, '')
            const isSending = useLocalStorage('is_sending', false);
            const isSent = useLocalStorage('is_sent', false);
            const countdown = useLocalStorage('countdown', 0);
            const intervalId = useLocalStorage('interval_id', null);

            const address = useLocalStorage(`coc_address_${id.value}`, '')
            const political_affiliation = useLocalStorage(`coc_political_affiliation_${id.value}`, '')
            const party_list = useLocalStorage(`coc_party_list_${id.value}`, '')
            const selected_position = useLocalStorage(`coc_selected_position_${id.value}`, '')

            const display_photo_base_64 = useLocalStorage(`coc_display_photo_base_64_${id.value}`, '')
            const display_photo_file = useLocalStorage(`coc_display_photo_file${id.value}`, '');
            const display_photo_file_name = useLocalStorage(`coc_display_photo_file_name_${id.value}`, '')

            const certification_of_grades_base_64 = useLocalStorage(`coc_certification_of_grades_base_64_${id.value}`, '')
            const certification_of_grades_file = useLocalStorage(`coc_certification_of_grades_file_${id.value}`, '')
            const certification_of_grades_file_name = useLocalStorage(`coc_certification_of_grades_file_name_${id.value}`, '')

            const is_submitting = ref(false)

            // watch for id changes then update the local storage by appending the new id
            watch(id, (newId, oldId) => {
                if (newId !== oldId) {
                    localStorage.setItem(`coc_student_number_${newId}`, student_number.value);
                    localStorage.setItem(`coc_verification_code_${newId}`, verification_code.value);
                    localStorage.setItem(`coc_address_${newId}`, address.value);
                    localStorage.setItem(`coc_political_affiliation_${newId}`, political_affiliation.value);
                    localStorage.setItem(`coc_party_list_${newId}`, party_list.value);
                    localStorage.setItem(`coc_selected_position_${newId}`, selected_position.value);

                    localStorage.setItem(`coc_display_photo_base_64_${newId}`, display_photo_base_64.value);
                    localStorage.setItem(`coc_display_photo_file${newId}`, display_photo_file.value);
                    localStorage.setItem(`coc_display_photo_file_name_${newId}`, display_photo_file_name.value);

                    localStorage.setItem(`coc_certification_of_grades_base_64_${newId}`, certification_of_grades_base_64.value);
                    localStorage.setItem(`coc_certification_of_grades_${newId}`, certification_of_grades_file.value);
                    localStorage.setItem(`coc_certification_of_grades_file_name_${newId}`, certification_of_grades_file_name.value);
                }
            });

            watch(political_affiliation, (newValue, oldValue) => {
                if (newValue !== oldValue) {
                    selected_position.value = '';
                }
            });

            // Convert the file to base64 string and lower quality version
            watch(display_photo_file, (newValue, oldValue) => {
                if (newValue && newValue instanceof Blob) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        const img = new Image();
                        img.onload = () => {
                            const canvas = document.createElement('canvas');
                            const ctx = canvas.getContext('2d');
                            
                            // Set the canvas dimensions to the image dimensions
                            canvas.width = img.width;
                            canvas.height = img.height;
                            
                            // Draw the image onto the canvas
                            ctx.drawImage(img, 0, 0, img.width, img.height);
                            
                            // Get a lower quality version of the image
                            const lowQualityImage = canvas.toDataURL('image/jpeg', .90);
                            
                            display_photo_base_64.value = lowQualityImage;
                        };
                        img.src = reader.result;
                    };
                    reader.readAsDataURL(newValue);
                }
            });

            // Convert the file to base64 string and lower quality version
            watch(certification_of_grades_file, (newValue, oldValue) => {
                if (newValue && newValue instanceof Blob) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        const img = new Image();
                        img.onload = () => {
                            const canvas = document.createElement('canvas');
                            const ctx = canvas.getContext('2d');
                            
                            // Set the canvas dimensions to the image dimensions
                            canvas.width = img.width;
                            canvas.height = img.height;
                            
                            // Draw the image onto the canvas
                            ctx.drawImage(img, 0, 0, img.width, img.height);
                            
                            // Get a lower quality version of the image
                            const lowQualityImage = canvas.toDataURL('image/jpeg', .90);
                            
                            certification_of_grades_base_64.value = lowQualityImage;
                        };
                        img.src = reader.result;
                    };
                    reader.readAsDataURL(newValue);
                }
            });

            // Set the file and file name when the user selects a file
            const handleDisplayPhotoFile = (event) => {
                const file = event.target.files[0];

                // Check if the file is an image.
                if (file.type && !file.type.startsWith('image/')) {
                    alert('File is not an image.');
                    return;
                }

                // Check the file size limit.
                if (file.size > 2 * 1024 * 1024) { // 2 MB
                    alert('File is too large. Please select an image less than 2 MB.');
                    return;
                }

                display_photo_file_name.value = file.name;
                display_photo_file.value = file;
            };

            // Set the file and file name when the user selects a file
            const handleCertificationFile = (event) => {
                const file = event.target.files[0];

                // Check if the file is an image.
                if (file.type && !file.type.startsWith('image/')) {
                    alert('File is not an image.');
                    return;
                }

                // Check the file size limit.
                if (file.size > 2 * 1024 * 1024) { // 2 MB
                    alert('File is too large. Please select an image less than 2 MB.');
                    return;
                }

                certification_of_grades_file_name.value = file.name;
                certification_of_grades_file.value = file;
            };

            // Fetch positions for the dropdown
            const fetchPositions = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/view/${id.value}`)

                return response.data.positions;
            }

            const { data: positionsData,
                    isLoading: isPositionsLoading,
                    isSuccess: isPositionsSuccess,
                    isError: isPositionsError, } =
                    useQuery({
                        queryKey: [`CoCPositions-${id.value}`],
                        queryFn: fetchPositions,
                    })

            return {
                id,
                electionName,
                student_number,
                verification_code,
                isSending,
                isSent,
                countdown,
                intervalId,
                address,
                political_affiliation,
                party_list,
                selected_position,
                is_submitting,

                display_photo_base_64,
                display_photo_file,
                display_photo_file_name,

                certification_of_grades_base_64,
                certification_of_grades_file,
                certification_of_grades_file_name,

                handleDisplayPhotoFile,
                handleCertificationFile,

                positionsData,
                isPositionsLoading,
                isPositionsSuccess,
                isPositionsError,
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
        created(){
            if (this.isSent) {
                this.intervalId = setInterval(() => {
                    if (this.countdown > 1) {
                        this.countdown--;
                    } 
                    else {
                        clearInterval(this.intervalId);
                        this.isSent = false;
                    }
                }, 1000);
            }
        },
        computed: {
            buttonText() {
                if (this.isSending) {
                    return 'Sending..';
                }
                else if (this.isSent) {
                    return `Resend in ${this.countdown} seconds`;
                }
                else {
                    return 'Send Code';
                }
            },
            submitStatus() {
                if (this.is_submitting) {
                    return 'Submitting..';
                }
                else {
                    return 'Submit';
                }
            },
        },
        methods:{
            returnPage(){
                router.visit(`/elections/view?id=${this.id}`)
            },
            clearLocalStorage() {
                localStorage.removeItem(`coc_student_number_${this.id.value}`);
                localStorage.removeItem(`coc_verification_code_${this.id.value}`);
                localStorage.removeItem(`coc_address_${this.id.value}`);
                localStorage.removeItem(`coc_political_affiliation_${this.id.value}`);
                localStorage.removeItem(`coc_party_list_${this.id.value}`);
                localStorage.removeItem(`coc_selected_position_${this.id.value}`);

                localStorage.removeItem(`coc_display_photo_base_64_${this.id.value}`);
                localStorage.removeItem(`coc_display_photo_file${this.id.value}`);
                localStorage.removeItem(`coc_display_photo_file_name_${this.id.value}`);

                localStorage.removeItem(`coc_certification_of_grades_base_64_${this.id.value}`);
                localStorage.removeItem(`coc_certification_of_grades_${this.id.value}`);
                localStorage.removeItem(`coc_certification_of_grades_file_name_${this.id.value}`);
            },
            sendCode() {
                if (this.student_number === '') {
                    return alert('Please enter your student number.')
                } 

                this.isSending = true;

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/code/generate`, {
                    student_number: this.student_number,
                    code_type: 'Verification'
                })
                .then((response) => {
                    console.log(response)
                    alert('The code has been sent to your email address.')

                    this.isSending = false;
                    this.isSent = true;
                    this.countdown = 30; // seconds
                    this.intervalId = setInterval(() => {
                        if (this.countdown > 1) {
                            this.countdown--;
                        } 
                        else {
                            clearInterval(this.intervalId);
                            this.isSent = false;
                        }
                    }, 1000);
                })
                .catch((error) => {
                    console.log(error)
                })

            },
            validate() {
                if (this.student_number === '') {
                    alert('Please enter your student number.')
                    return false
                } 

                if (this.verification_code === '') {
                    alert('Please enter your verification code.')
                    return false
                }

                if (this.address === '') {
                    alert('Please enter your address.')
                    return false
                }

                if (this.political_affiliation === '') {
                    alert('Please select your political affiliation.')
                    return false;
                }

                if (this.political_affiliation === 'Independent') {
                    if (this.selected_position === '') {
                        alert('Please select your position.')
                        return false;
                    }
                }
                else if (this.political_affiliation === 'Party List') {
                    if (this.party_list === '') {
                        alert('Please select your party list.')
                        return false;
                    }

                    if (this.selected_position === '') {
                        alert('Please select your position.')
                        return false;
                    }
                }

                if (this.display_photo_file === '') {
                    alert('Please upload your display photo.')
                    return false;
                }

                if (this.certification_of_grades_file === '') {
                    alert('Please upload your certification of grades.')
                    return false;
                }

                return true;
            },
            submit() {
                if (this.validate()) {
                    const formData = new FormData();
                    formData.append('election_id', Number(this.id));
                    formData.append('student_number', this.student_number);
                    formData.append('verification_code', this.verification_code);
                    formData.append('address', this.address);
                    formData.append('political_affiliation', this.political_affiliation);
                    formData.append('party_list', this.party_list);
                    formData.append('position', this.selected_position);

                    formData.append('display_photo', this.display_photo_base_64);
                    formData.append('display_photo_file_name', this.display_photo_file_name)

                    formData.append('certification_of_grades', this.certification_of_grades_base_64);
                    formData.append('certification_of_grades_file_name', this.certification_of_grades_file_name)

                    this.is_submitting = true;

                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/coc/submit`, formData)
                    .then((response) => {
                        console.log(response.data)
                        alert('Your certificate of candidacy has been submitted.')

                        this.clearLocalStorage()
                        router.visit(`/elections/view?id=${this.id}`)
                    })
                    .catch((error) => {
                        alert(error.response.data.error)
                        console.log(error)
                    })
                    .finally(() => {
                        this.is_submitting = false;
                    });
                }
            },
            beforeDestroy() {
                if (this.intervalId) {
                    clearInterval(this.intervalId);
                }
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