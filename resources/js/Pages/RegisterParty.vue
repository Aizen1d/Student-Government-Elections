<template>
    <title>Register Party - COMELEC Portal</title>
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
                <div class="col-6 mb-4">
                    <div class="components row">
                        <span class="header-label">Party List Information</span>

                        <div>
                            <label class="form-label" for="name">Party Name {{ party_input_status }}</label>
                            <input class="form-control" type="text" name="name" placeholder="Enter your party's name" @keyup="checkPartyDebounce" :disabled="is_submitting" v-model="party_name">
    
                            <label class="form-label mt-4" for="email">Email Address</label>
                            <input class="form-control" type="email" name="email" placeholder="Enter your party's email address" :disabled="is_submitting" v-model="email">
    
                            <label class="form-label mt-4" for="contact">Cellphone Number</label>
                            <input class="form-control" type="text" @keypress="cellphone_number_filter" name="contact" placeholder="Enter your party's cellphone number" :disabled="is_submitting" v-model="cellphone_number">
    
                            <label for="desc" class="form-label mt-4">Description</label>
                            <textarea class="form-control" type="text" name="desc" placeholder="Enter your party's description" :disabled="is_submitting" v-model="description"></textarea>
    
                            <label for="mission" class="form-label mt-4">Mission</label>
                            <textarea class="form-control" type="text" name="mission" placeholder="Enter your party's mission" :disabled="is_submitting" v-model="mission"></textarea>
    
                            <label for="vision" class="form-label mt-4">Vision</label>
                            <textarea class="form-control" type="text" name="vision" placeholder="Enter your party's vision" :disabled="is_submitting" v-model="vision"></textarea>
    
                            <label for="plat" class="form-label mt-4">Platforms</label>
                            <textarea class="form-control mb-2" type="text" name="plat" placeholder="Enter your party's platform" :disabled="is_submitting" v-model="platforms"></textarea>
                        </div>
                    </div>
                </div>

                <div class="col-6">
                    <div class="components1 row">
                        <span class="header-label">Image Attachment (Optional)</span>
                        
                        <div v-if="image_base_64">
                            <img :src="image_base_64" alt="Image attachment" style="width: 100%; height: 100%; margin-top: 0.5%;">
                        </div>
                        
                        <div class="row my-4">
                            <div class="col-4">
                                <label for="image-file-upload" class="image-file-upload" :style="{ marginLeft: image_base_64 ? '32%' : '0%' }">
                                    Select File
                                </label>
                                <input id="image-file-upload" type="file" accept="image/*" style="display: none;" :disabled="is_submitting" @change="handleImageAttachmentFile">
                            </div>
                            <div class="col-8" style="display: flex; align-items: center;">
                                <label class="mx-1 my-2 text-truncate" style="max-width: 100%;">
                                    {{ image_file_name }}
                                </label>
                                <button class="remove-button" :disabled="is_submitting" v-if="image_base_64" @click.prevent="clearImageAttachment" 
                                        style="background-color: rgb(214, 212, 212); 
                                        border: none;
                                        color: white;
                                        border-radius: 50%;
                                        width: 2em;
                                        height: 2em;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        margin-left: 1%;"><img src="../../images/Elections/Partylist/close.svg" alt="" style="width: 13px; margin: 0; filter: brightness(0) saturate(100%) invert(100%) sepia(4%) saturate(4406%) hue-rotate(247deg) brightness(110%) contrast(100%);">
                                </button>
                            </div>
                        </div>
                    </div>   
                    
                    <div class="components row my-4">
                        <span class="header-label">Certification of Grades</span>
                        <div>
                            <div class="" v-if="video !== '' && video.startsWith('https://www.youtube.com/watch?v=')">
                                <iframe v-show="!videoLoadingState" @load="videoLoaded" style="margin-bottom: 1%;" width="100%" height="350px" :src="getEmbedUrl(video)" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                            </div>
                            <ImageSkeleton v-if="videoLoadingState && video.startsWith('https://www.youtube.com/watch?v=')" 
                                    :loading="videoLoadingState" 
                                    :itemCount="1" 
                                    :borderRadius="'0px'"
                                    :imageWidth="'32vw'" 
                                    :imageHeight="'37vh'"
                                    :containerMargin="'1% 10%'"
                                    :itemMargin="'0em'">
                            </ImageSkeleton>
        
                            <label class="form-label" for="youtube-link">Youtube Link (must be embeddable)</label>
                            <input class="form-control mb-2" type="text" name="youtube-link" placeholder="Enter youtube video link" :disabled="is_submitting" v-model="video">
                        </div>
                        
                    </div> 
                    
                    <div class="buttons">
                        <button class="cancel-button" :disabled="is_submitting" @click.prevent="returnPage">Cancel</button>
                        <button class="submit-button" :disabled="is_submitting" @click.prevent="submit">Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue'
    import Standards from '../Shared/Standards.vue'
    import ActionButton from '../Shared/ActionButton.vue'

    import { ref, watch } from 'vue'
    import { router } from '@inertiajs/vue3';
    import { useLocalStorage } from '@vueuse/core';
    import ImageSkeleton from '../Skeletons/ImageSkeleton.vue';
    import axios from 'axios'

    export default {
        setup(props) {
            const id = ref(Number(props.id))
            const electionName = ref(props.electionName)

            const party_name = useLocalStorage(`party_list_party_name_${id.value}`, '')
            const email = useLocalStorage(`party_list_email_${id.value}`, '')
            const cellphone_number = useLocalStorage(`party_list_cellphone_number_${id.value}`, '')
            const description = useLocalStorage(`party_list_description_${id.value}`, '')
            const mission = useLocalStorage(`party_list_mission_${id.value}`, '')
            const vision = useLocalStorage(`party_list_vision_${id.value}`, '')
            const platforms = useLocalStorage(`party_list_platforms_${id.value}`, '')

            const image_base_64 = useLocalStorage(`party_list_image_base_64_${id.value}`, '')
            const image_file = ref(null)
            const image_file_name = useLocalStorage(`party_list_image_file_name_${id.value}`, '')
            const video = useLocalStorage(`party_list_video_${id.value}`, '')
            const videoLoadingState = ref(true)

            const party_input_status = useLocalStorage(`party_list_party_input_status_${id.value}`, '')
            const submittable = useLocalStorage(`party_list_submittable_${id.value}`, false)
            const is_submitting = ref(false)

            // watch for id changes then update the local storage by appending the new id
            watch(id, (newId, oldId) => {
                if (newId !== oldId) {
                    localStorage.setItem(`party_list_party_name_${newId}`, party_name.value)
                    localStorage.setItem(`party_list_email_${newId}`, email.value)
                    localStorage.setItem(`party_list_cellphone_number_${newId}`, cellphone_number.value)
                    localStorage.setItem(`party_list_description_${newId}`, description.value)
                    localStorage.setItem(`party_list_mission_${newId}`, mission.value)
                    localStorage.setItem(`party_list_vision_${newId}`, vision.value)
                    localStorage.setItem(`party_list_platforms_${newId}`, platforms.value)

                    localStorage.setItem(`party_list_image_base_64_${newId}`, image_base_64.value)
                    localStorage.setItem(`party_list_image_file_name_${newId}`, image_file_name.value)

                    localStorage.setItem(`party_list_video_${newId}`, video.value)
                }
            })

            watch(image_file, (newValue, oldValue) => {
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
                            
                            image_base_64.value = lowQualityImage;
                        };
                        img.src = reader.result;
                    };
                    reader.readAsDataURL(newValue);
                }
            });

            // watch for changes in the video link then set the video loading state to true
            watch(video, (newValue, oldValue) => {
                if (newValue !== oldValue) {
                    videoLoadingState.value = true;
                }
            });

            const cellphone_number_filter = (event) => {
                const pattern = /[0-9]/;
                const inputChar = String.fromCharCode(event.charCode);

                if (cellphone_number.value.length >= 11) {
                    event.preventDefault();
                }

                if (!pattern.test(inputChar)) {
                    event.preventDefault();
                }
            };

            const handleImageAttachmentFile = (event) => {
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
               
                image_file_name.value = file.name;
                image_file.value = file;
            };

            let timeoutId;

            const checkPartyDebounce = () => {
                if (party_name.value === '') {
                    party_input_status.value = '';
                    submittable.value = false;
                    return;
                }

                party_input_status.value = '(Checking eligibility..)';

                clearTimeout(timeoutId);
                timeoutId = setTimeout(checkIfPartyNameEligible, 500);
            };

            const checkIfPartyNameEligible = async () => {
                await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/is-taken/${party_name.value}`)
                    .then((response) => {
                        if (response.data === true) {
                            party_input_status.value = '(Already taken)';
                            submittable.value = false;
                        }
                        else {
                            party_input_status.value = '(Eligible)';
                            submittable.value = true;
                        }
                    })
                    .catch((error) => {
                        console.log(error)
                    });
            }

            return {
                id,
                electionName,

                party_name,
                email,
                cellphone_number,
                description,
                mission,
                vision,
                platforms,
                image_base_64,
                image_file,
                image_file_name,
                video,
                videoLoadingState,
                party_input_status,
                submittable,
                is_submitting,

                cellphone_number_filter,
                handleImageAttachmentFile,
                checkPartyDebounce
            }
        },
        props: {
            id: '',
            electionName: 'ss',
        },
        components: {
            Navbar,
            Standards,
            ActionButton,
            ActionButton,
            ImageSkeleton,
        },
        methods: {
            returnPage(){
                router.visit(`/elections/view?id=${this.id}`)
            },
            getEmbedUrl(url) {
                let videoId = url.split('v=')[1];
                
                return 'https://www.youtube.com/embed/' + videoId;
            },
            videoLoaded(){
                this.videoLoadingState = false;
            },
            clearImageAttachment() {
                this.image_base_64 = '';
                this.image_file_name = '';
            },
            clearLocalStorage() {
                localStorage.removeItem(`party_list_party_name_${this.id}`);
                localStorage.removeItem(`party_list_email_${this.id}`);
                localStorage.removeItem(`party_list_cellphone_number_${this.id}`);
                localStorage.removeItem(`party_list_description_${this.id}`);
                localStorage.removeItem(`party_list_mission_${this.id}`);
                localStorage.removeItem(`party_list_vision_${this.id}`);
                localStorage.removeItem(`party_list_platforms_${this.id}`);
                
                localStorage.removeItem(`party_list_image_base_64_${this.id}`);
                localStorage.removeItem(`party_list_image_file_name_${this.id}`);

                localStorage.removeItem(`party_list_video_${this.id}`);
            },
            validate() {
                if (this.party_name === '') {
                    alert('Party name is required.');
                    return false;
                }

                if (this.submittable === false) {
                    alert('Party name is already taken.');
                    return false;
                }

                // check if valid email
                if (this.email === '') {                    
                    alert('Email is required.');
                    return false;
                }
                else {
                    let re = /\S+@\S+\.\S+/;
                    if (!re.test(this.email)) {
                        alert('Invalid email address.');
                        return false;
                    }
                }

                if (this.cellphone_number === '') {
                    alert('Cellphone number is required.');
                    return false;
                }
                else if (this.cellphone_number.length < 11) {
                    alert('Cellphone number must be 11 digits.');
                    return false;
                }

                if (this.description === '') {
                    alert('Description is required.');
                    return false;
                }

                if (this.mission === '') {
                    alert('Mission is required.');
                    return false;
                }

                if (this.vision === '') {
                    alert('Vision is required.');
                    return false;
                }

                if (this.platforms === '') {
                    alert('Platforms is required.');
                    return false;
                }

                return true;
            },
            submit() {
                if (this.validate()) {
                    let formData = new FormData();
                    formData.append('election_id', this.id);
                    formData.append('party_name', this.party_name);
                    formData.append('email_address', this.email);
                    formData.append('cellphone_number', this.cellphone_number);
                    formData.append('description', this.description);
                    formData.append('mission', this.mission);
                    formData.append('vision', this.vision);
                    formData.append('platforms', this.platforms);

                    if (this.image_base_64 !== '') {
                        formData.append('image_attachment', this.image_base_64);
                        formData.append('image_file_name', this.image_file_name)
                    }
                    if (this.video !== '' && this.video.startsWith('https://www.youtube.com/watch?v=') ) {
                        formData.append('video_attachment', this.video);
                    }

                    const confirm = window.confirm('Are you sure you want to submit this partylist?');
                    if (!confirm) {
                        return;
                    }

                    if (this.is_submitting) {
                        return;
                    }

                    this.is_submitting = true;

                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/partylist/submit`, formData, {
                        })
                        .then((response) => {
                            console.log(response.data)
                            this.clearLocalStorage();

                            alert('Partylist submitted.')
                            router.visit(`/elections/view?id=${this.id}`)
                        })
                        .catch((error) => {
                            console.log(error)
                            alert(error.response.data.error)
                        })
                        .finally(() => {
                            this.is_submitting = false;
                        });
                }
            }
        }
    }

</script>

<style scoped>
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

    .form-label, .form-control{
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

    .submit-button:disabled{
        background-color: #a2a2a2;
        cursor: default;
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

    .header-label{
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 22px;
        margin-right: auto;
    }

    .remove-button:hover{
        background-color: #a2a2a2 !important;
    }

    .image-file-upload {
        padding: 7px;
        width: 70%;
        font-size: 100%;
        border: 1px solid #ccc;
        border-radius: 8px;
        display: inline-block;
        cursor: pointer;
        text-align: center;
    }

    .image-file-upload:disabled {
        background-color: #4d4d4d;
        cursor: default;
    }

    .remove-button:disabled {
        background-color: #ccc !important;
        cursor: default;
    }

    .components textarea{
        resize: none;
        overflow-y: auto;
        height: 150px;
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