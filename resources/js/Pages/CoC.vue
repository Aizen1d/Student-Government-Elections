<template>
        <title>File CoC - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="current-page">
            <span class="header" @click.prevent="returnPage">ONGOING ELECTIONS</span> 
            <span class="arrow"> ></span>
            {{ electionName }}
            <span class="arrow"> ></span>
            FILE CERTIFICATE OF CANDIDACY
        </h1>

        <div class="main">
            <div class="row g-4">
                <div class="col-6">
                    <div class="note">
                        <img src="../../images/Elections/CoC/information.svg" alt="" class="information-svg">
                        <span>
                            To file a certificate of candidacy, submit your student number. 
                            An email with a verification code will be sent to your associated email. Use this code to verify.  
                        </span>
                    </div>
                    <div class="components row">
                        <span class="header-label">Applicant Information</span>

                        <label class="form-label" for="student-number">Student Number</label>
                        <div class="col-8">
                            <input class="form-control" maxlength="15" placeholder="Enter your student number" type="text" name="student-number" :disabled="is_submitting" v-model="student_number">
                        </div>
                        <div class="col-4">
                            <button class="code-button" @click.prevent="sendCode" :disabled="isSending || isSent || is_submitting" 
                                    style="font-size: 1em;">{{ buttonText }}
                            </button>
                        </div>

                        <div>
                            <label class="form-label mt-4" for="code">Verification Code</label>
                            <input class="form-control" placeholder="Enter verification code" :disabled="is_submitting" v-model="verification_code" type="text" name="code">
                        </div>
                    </div>   
                    
                    <div class="components row my-4">
                        <span class="header-label">Election Information</span>
                        <div class="col info">
                            <label class="form-label" for="selected">Political Affiliation</label>
                            <input type="hidden" name="requirements">
                            <select class="form-select" aria-label="Default select example" :disabled="is_submitting" v-model="political_affiliation">
                                <option value="" hidden selected>Select</option>
                                <option selected>Independent</option>
                                <option selected>Partylist</option>
                            </select>

                            <div v-if="political_affiliation !== '' && political_affiliation !== 'Independent'">
                                <label class="form-label mt-4">Select Partylist</label>
                                <input type="hidden" name="requirements">
                                <select class="form-select" aria-label="Default select example" :disabled="is_submitting" v-model="party_list">
                                    <option value="" hidden selected>Select</option>
                                    <option v-for="(party, index) in partyListsData" :key="index" :value="party.PartyListName">{{ party.PartyListName }}</option>
                                </select>
                            </div>

                            <div v-if="political_affiliation !== ''">
                                <label class="form-label mt-4">Select Position</label>
                                <input type="hidden" name="requirements">
                                <select class="form-select" aria-label="Default select example" :disabled="is_submitting" v-model="selected_position">
                                    <option value="" hidden selected>Select</option>
                                    <option v-for="(position, index) in positionsData" :key="index" :value="position.PositionName">{{ position.PositionName }}</option>
                                </select>
                            </div>

                            <label class="form-label mt-4" for="motto">Motto (Optional)</label>
                            <input class="form-control margin1" placeholder="Enter your motto" type="text" name="motto" :disabled="is_submitting" v-model="motto">
                            
                            <label class="form-label" for="platform">Platforms</label>
                            <textarea class="form-control padding1 platform" placeholder="Enter your platforms" type="text" name="platform" :disabled="is_submitting" v-model="platforms"></textarea>
                        </div>
                    </div>     
                </div>

                <div class="col-6">
                    <div class="components1 row">
                        <span class="header-label">Display Photo</span>

                        <div class="upload">
                            <img v-if="display_photo_base_64" :src="display_photo_base_64" alt="" class="organization-logo" draggable="false">
                            <img v-else src="../../images/Elections/CoC/default.png" alt="" class="organization-logo" draggable="false">
                            <div class="round">
                                <input type="file" accept="image/*" :disabled="is_submitting" @change="handleDisplayPhotoFile">
                                <i class="fa fa-camera" style = "color: #000000;"></i>
                            </div>
                        </div>
                    </div>   
                    
                    <div class="components row my-4">
                        <span class="header-label">Certification of Grades</span>
                        <div>
                            <input class="form-control mb-3" type="file" name="grades" accept="image/*" :disabled="is_submitting" @change="handleCertificationFile">
                        </div>
                        <div v-if="certification_of_grades_base_64">
                            <img :src="certification_of_grades_base_64" alt="Certification of Grades" style="width: 90%; height: auto; margin-left: 5%; margin-top: 1%;" >
                        </div>
                    </div> 
                    
                    <div class="buttons">
                        <button class="cancel-button" :disabled="is_submitting" @click.prevent="returnPage">Cancel</button>
                        <button class="submit-button" :disabled="is_submitting" @click.prevent="submit">{{ submitStatus }}</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
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
            const isSending = useLocalStorage(`is_sending_${id.value}`, false);
            const isSent = useLocalStorage(`is_sent_${id.value}`, false);
            const countdown = useLocalStorage('countdown', 0);
            const intervalId = useLocalStorage('interval_id', null);

            const motto = useLocalStorage(`coc_motto_${id.value}`, '')
            const platforms = useLocalStorage(`coc_platforms_${id.value}`, '')
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
                    localStorage.setItem(`coc_motto_${newId}`, motto.value);
                    localStorage.setItem(`coc_platforms_${newId}`, platforms.value);
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
                    party_list.value = '';
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

            // Fetch party lists for the dropdown
            const fetchPartyLists = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/approved/all`)

                return response.data.partylists;
            }

            const { data: partyListsData,
                    isLoading: isPartyListsLoading,
                    isSuccess: isPartyListsSuccess,
                    isError: isPartyListsError, } =
                    useQuery({
                        queryKey: [`PartyLists-${id.value}`],
                        queryFn: fetchPartyLists,
                    })

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
                motto,
                platforms,
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

                partyListsData,
                isPartyListsLoading,
                isPartyListsSuccess,
                isPartyListsError,

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
                localStorage.removeItem(`coc_student_number_${this.id}`);
                localStorage.removeItem(`coc_verification_code_${this.id}`);
                localStorage.removeItem(`coc_motto_${this.id}`);
                localStorage.removeItem(`coc_platforms_${this.id}`);
                localStorage.removeItem(`coc_political_affiliation_${this.id}`);
                localStorage.removeItem(`coc_party_list_${this.id}`);
                localStorage.removeItem(`coc_selected_position_${this.id}`);

                localStorage.removeItem(`coc_display_photo_base_64_${this.id}`);
                localStorage.removeItem(`coc_display_photo_file${this.id}`);
                localStorage.removeItem(`coc_display_photo_file_name_${this.id}`);

                localStorage.removeItem(`coc_certification_of_grades_base_64_${this.id}`);
                localStorage.removeItem(`coc_certification_of_grades_${this.id}`);
                localStorage.removeItem(`coc_certification_of_grades_file_name_${this.id}`);
            },
            sendCode() {
                if (this.student_number === '') {
                    return alert('Please enter your student number.')
                } 

                this.isSending = true;

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/code/coc/verification/generate`, {
                    student_number: this.student_number,
                    code_type: 'Verification'
                })
                .then((response) => {
                    // console.log(response) // commented out because code can be seen in the console
                    alert(`Verification code sent to your email ${response.data.email_address}`)

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

                    alert(error.response.data.error) 
                    this.isSending = false;
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
                    formData.append('motto', this.motto);
                    formData.append('platforms', this.platforms);
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
                        this.clearLocalStorage()

                        alert('Your certificate of candidacy has been submitted.')

                        this.$nextTick(() => {
                            router.visit(`/elections/view?id=${this.id}`)
                        })
                    })
                    .catch((error) => {
                        console.log(error)

                        const errorMessage = error.response.data.error;
                        alert(errorMessage)
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

    .information-svg{
        width: 30px;
        height: 30px;
        margin-right: 10px;
    }

    .note{
        background-color: #F2F2F2;
        padding: 2%;
        font-size: 16px;
        display: flex;
        align-items: center;
    }

    .components{
        background-color: white;
        padding: 3%;
        display: flex;
        align-items: center;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        margin: 0%;
    }

    .components1{
        background-color: white;
        padding: 3%;
        display: flex;
        align-items: center;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        margin: 0%;
        flex-direction: column;
        justify-content: center;
    }

    .margin{
        margin-bottom: 4%;
    }

    .margin1{
        margin-bottom: 3%;
    }

    .padding{
        margin-bottom: 1%;
    }

    .padding1{
        margin-bottom: 0.8%;
    }

    .form-label, .form-control, .form-select{
        font-size: 18px;
    }

    .code-button{
        width: 100%;
        height: 100%;
        border: transparent;
        border-radius: 6px;
        background-color: #730000;
        color: white;
        align-items: end;
        padding: 0%;
        font-size: 18px;
    }

    .buttons{
        background-color: white;
        padding: 3%;
        display: flex;
        align-items: center;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        justify-content: space-between;
    }

    .submit-button{
        border: transparent;
        border-radius: 6px;
        background-color: #730000;
        color: white;
        align-items: end;
        padding: 1.5%;
        font-size: 18px;
        width: 150px;
    }

    .cancel-button{
        padding: 1.5%;
        border: transparent;
        border-radius: 10px;
        font-size: 18px;
        background-color: transparent;
        color: #CC3300;
    }

    .row{
        align-items: stretch;
    }

    .upload{
        width: 135px;
        position: relative;
        padding: 0%;
        margin: auto;
    }
    
    .upload img{
        height: 135px;
        border-radius: 50%;
        border: 6px solid #eaeaea;
        object-fit: cover;
    }
    
    .upload .round{
        position: absolute;
        bottom: 0;
        right: 0;
        background: #D9D9D9;
        width: 32px;
        height: 32px;
        line-height: 33px;
        text-align: center;
        border-radius: 50%;
        overflow: hidden;
    }
    
    .upload .round input[type = "file"]{
        position: absolute;
        transform: scale(2);
        opacity: 0;
    }

    input[type=file]::-webkit-file-upload-button{
        cursor: pointer;
    }

    .organization-logo{
        width: 100%;
        height: 100%;
    }

    .header-label{
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 22px;
        margin-right: auto;
    }

    .platform{
        resize: none;
        overflow-y: auto;
        height: 200px;
    }
</style>