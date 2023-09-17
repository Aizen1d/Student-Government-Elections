<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Announcements</h2>
            </div>
            <div class="col-6 new">
                <ActionButton :disabled="new_button_disabled" class="new-btn">New Announcement</ActionButton>
            </div>
        </div>

        <BaseContainer>
            <form @submit.prevent="save">
                <div class="form-group row">
                    <div class="col-2">
                        <label class="form-label" for="selected">Type of Announcement</label>
                        <input type="hidden" name="announcement-type">
                        <select class="form-select" aria-label="Default select example" v-model="type_select">
                            <option value="" disabled hidden selected>Select Type</option>
                            <option value="election">Election</option>
                            <option value="debate">Debate</option>
                            <option value="open">Open Forum</option>
                            <option value="educational-program">Educational Program</option>
                            <option value="results">Results</option>
                        </select>
                    </div>
                    <div class="col-8">
                        <label class="form-label" for="title">Title</label>
                        <input class="form-control" type="title" name="title" v-model="title_input">
                    </div>
                    <div class="col-2">
                        <label class="form-label" for="id">ID</label>
                        <input class="form-control" type="id" name="id" v-model="count_input" readonly>
                    </div>
                </div>

                <div>
                    <div class="form-group">
                        <label for="body" class="form-label">Body</label>
                        <textarea class="form-control body" type="text" name="selected-body" v-model="body_input"></textarea>
                    </div>
                </div>

                <div>
                    <h6 class="section-title">Attachments</h6>
                    <div class="form-group col-2">
                        <label class="form-label" for="selected">Type of Attachment</label>
                        <input type="hidden" name="attachment-type">
                        <select class="form-select" aria-label="Default select example" v-model="type_of_attachment">
                            <option value="0" selected>Select</option>
                            <option value="Banner">Banner</option>
                            <option value="Poster">Poster</option>
                        </select>
                    </div>
                    <div class="form-group col-2" v-if="type_of_attachment !== '0'">
                        <label class="form-label" for="selected">Upload Image</label>
                        <input type="file" name="attachment" class="form-control" ref="fileInput" @change="onFileChange">                    
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <button class="delete-btn">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <ActionButton @submit.prevent="save" class="save-btn">Save</ActionButton>
                    </div>
                </div>
            </form>
        </BaseContainer>

        <BaseContainer>
            <BaseTable :columns="['ID', 'Type', 'Title']">
                <tr v-for="(item, index) in items" :key="index" @click="selectItem(item)" 
                    v-bind:class="{ 'active-row': selectedItem && selectedItem.id === item.id && selectedItem.type === item.type }">
                    <td class="my-cell">{{ item.count }}</td>
                    <td class="my-cell">{{ item.type.charAt(0).toUpperCase() + item.type.slice(1) }}</td>
                    <td class="my-cell">{{ item.title }}</td>
                </tr>
            </BaseTable>
        </BaseContainer>

    </div>
</template>

<script>
import Navbar from '../../Shared/Navbar.vue';
import Sidebar from '../../Shared/Sidebar.vue';
import BaseTable from '../../Shared/BaseTable.vue';
import BaseContainer from '../../Shared/BaseContainer.vue';
import ActionButton from '../../Shared/ActionButton.vue';

import axios from 'axios';
import { ref } from 'vue';


export default {
    setup() {
        const type_select = ref('');
        const title_input = ref('');
        const id_input = ref('');
        const count_input = ref('');
        const body_input = ref('');
        const type_of_attachment = ref('0');
        const upload_image_attachment = ref('');
        const fileInput = ref(null);
        const new_button_disabled = ref(true);
        const saving = ref(false);

        // Data for the table
        const items = ref([]);

        return {
            type_select,
            title_input,
            id_input,
            count_input,
            body_input,
            type_of_attachment,
            upload_image_attachment,
            fileInput,
            new_button_disabled,
            saving,
            items,
        }
    },
    components: { Navbar, Sidebar, BaseTable, BaseContainer, ActionButton },
    created() {
        axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/id/latest`)
            .then(response => {
                this.count_input = "Announcement #" + (response.data.id + 1);
            })
            .catch(error => {
                console.log(error);
            });
    },
    methods: {
        onFileChange(event) {
            this.upload_image_attachment = event.target.files[0];
        },
        save() {
            if (this.type_select.trim().length < 1) {
                return alert('Please select a type');
            }
            else if (this.title_input.trim().length < 1) {
                return alert('Please input a title');
            }
            else if (this.title_input.trim().length > 255) {
                return alert('Title is too long, 255 characters only');
            }
            else if (this.body_input.trim().length < 1) {
                return alert('Please input a body');
            }

            if (this.type_of_attachment !== '0') {
                if (this.upload_image_attachment === '') {
                    return alert('Please upload an image');
                }
            }

            // Create a FormData object
            let formData = new FormData();

            // Append the form fields to the FormData object
            formData.append('type_select', this.type_select);
            formData.append('title_input', this.title_input);
            formData.append('body_input', this.body_input);
            formData.append('type_of_attachment', this.type_of_attachment);

            // If an image file is selected, append it to the FormData object
            if (this.type_of_attachment !== '0' && this.$refs.fileInput.files[0]) {
                formData.append('attachment_image', this.$refs.fileInput.files[0]);
            }

            axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/save`, formData, {
                
                }).then(response => {
                    console.log(response.data.form_data);
                    console.log(response.data.image_details);

                    alert('Announcement saved successfully')

                }).catch(error => {
                    console.error(error);
                });
                
        }
    },
}

</script>

<style scoped>
.components {
    margin-left: 18%;
    margin-top: 2%;
    font-family: 'Source Sans', sans-serif;
    margin-right: 3.2%;
}

.components h2 {
    font-weight: 800;
    font-size: 28px;
}

.form-control, .form-select, .body {
    border: 1px solid rgba(40, 40, 40, 0.25);
}

.new {
    margin-top: -1%;
    text-align: end;
}

.body {
    resize: none;
    overflow-y: auto;
    height: 200px;
}

.form-group {
    padding-bottom: 15px;
}

.new-btn{
    margin-top: 1.5%;
}

.new-btn:disabled{
    background-color: #cccccc;
}

.save {
    text-align: right;
}

.save-btn{
    margin-top: 1.5%;
}

.delete-btn {
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 20px 15px 20px;
    border: transparent;
    border-radius: 10px;
    background-color: transparent;
    color: #CC3300;
}

.delete-btn:hover{
    color: #B90321;
}

.head {
    text-align: center;
}

.section-title {
    font-weight: bolder;
    margin-top: 1%;
}
</style>