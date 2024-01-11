<template>
    <div class="appeal-modal" v-show="isModalOpen">
        <div class="appeal-content">
            <div class="appeal-header">
                <h1 class="header-label">File an Appeal</h1>
            </div>
            
            <label class="form-label" for="name">Student Number <ToolTip class="mx-2"><slot>Linked email of this student number will be used when appeal is submitted.</slot></ToolTip></label>
            <input v-model="student_number" :disabled="submitting" class="form-control margin" style="border: 1px solid #c2c2c2;" type="text" name="name" maxlength="15">

            <label for="desc" class="form-label">Appeal details</label>
            <textarea v-model="appeal_details" :disabled="submitting" class="form-control margin details" type="text" name="desc"></textarea>

            <label class="form-label">Upload Attachment <span style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;">(Optional. 3mb max)</span> <ToolTip class="mx-2"><slot>If you have multiple images to provide, please compile it in pdf.</slot></ToolTip></label>
            <input ref="attachment" @change="updateAttachment" :disabled="submitting" type="file" accept="image/*,.pdf" style="border: 1px solid #c2c2c2;" name="attachment" class="form-control">

            <div class="appeal-buttons">
                <button class="cancel-button" :disabled="submitting" @click.prevent="closeModal">Cancel</button>
                <ActionButton class="submit-button" :disabled="submitting" @click.prevent="submit">Submit</ActionButton>
            </div>
        </div>
    </div>
    <ActionButton class="appeal-button" v-show="!isModalOpen" @click="openModal">
        <i class="fas fa-flag" style="color: #ffffff;"></i>
    </ActionButton>
</template>

<script>
    import ActionButton from '../Shared/ActionButton.vue'
    import ToolTip from '../Shared/Tooltip.vue'

    import { ref } from 'vue'
    import axios from 'axios'

    export default {
        setup(){
            const isModalOpen = ref(false);

            const student_number = ref('');
            const appeal_details = ref('');
            const attachment = ref('');

            const submitting = ref(false);

            return{
                isModalOpen,
                student_number,
                appeal_details,
                attachment,
                submitting,
            }
        },
        components: {
            ActionButton,
            ToolTip,
        },
        methods: {
            openModal(){
                this.isModalOpen = true;
            },
            closeModal(){
                this.isModalOpen = false;
            },
            clearInputs(){
                this.student_number = '';
                this.appeal_details = '';
                
                this.attachment = null;
                this.$refs.attachment.value = '';
            },
            updateAttachment(event) {
                const reader = new FileReader();
                reader.onload = e => {
                    this.attachment = e.target.result;
                };
                reader.readAsDataURL(event.target.files[0]);
            },
            verifyInputs() {
                if (this.student_number === '') {
                    alert('Please enter your student number.');
                    return false;
                }
                if (this.appeal_details === '') {
                    alert('Please enter your appeal details.');
                    return false;
                }
                if (this.attachment !== '') {
                    if (this.attachment.size > 1024 * 1024 * 3) {
                        alert('File size exceeds 3mb.');
                        return false;
                    }
                }

                return true;
            },
            submit() {
                if (this.verifyInputs()) {
                    const data = {
                        student_number: this.student_number,
                        appeal_details: this.appeal_details,
                        attachment: this.attachment,
                    }

                    this.submitting = true;
                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election-appeals/submit`, data)
                    .then(response => {
                        alert('Appeal submitted successfully.');
                        this.closeModal();
                        this.clearInputs();
                    })
                    .catch(error => {
                        if (error.response.data.error) {
                            alert(error.response.data.error);
                        }
                        else {
                            alert('An error occured while submitting your appeal.');
                        }
                    })
                    .finally(() => {
                        this.submitting = false;
                    })
                }
            }
        }
    }
</script>

<style scoped>
    .appeal-modal{
        display: block;
        position: fixed;
        z-index: 99;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.4);
    }

    .appeal-content{
        position: fixed;
        right: 0;
        bottom: 0;
        z-index: 98;
        width: 500px; /* Adjust as needed */
        height: auto; /* Adjust as needed */
        background-color: rgb(255, 255, 255);
        font-family: 'Inter', sans-serif;
        padding: 1.5%;
        border-radius: 5px;
    }

    .header-label{
        font-size: 30px;
        color: #800000;
        margin-bottom: 5%;
        text-align: center;
        font-weight: 600;
    }

    .margin{
        margin-bottom: 4%;
    }

    .details{
        background-color: white;
        border: 1px solid #c2c2c2;
        resize: none;
        overflow-y: auto;
        height: 150px;
    }

    .appeal-buttons{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 6%;
    }

    .cancel-button{
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 15px 20px 15px 20px;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
        width: fit-content;
    }

    .submit-button{
        font-family: 'Inter', sans-serif !important;
    }

    .appeal-button {
        position: fixed;
        right: 20px;
        bottom: 20px;
        padding: 0%;
        width: 52px !important;
        height: 50px !important;
        z-index: 98;
        border-radius: 50px !important
    }

</style>