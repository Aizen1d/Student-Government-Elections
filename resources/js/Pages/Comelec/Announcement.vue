<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Announcements</h2>
            </div>
            <div class="col-6 new">
                <ActionButton :disabled="new_button_disabled" class="new-btn" @click="newButtonSelected">New Announcement</ActionButton>
            </div>
        </div>

        <BaseContainer :height="'auto'">
            <form @submit.prevent="save">
                <div class="form-group row">
                    <div class="col-2">
                        <label class="form-label" for="selected">Type of Announcement</label>
                        <input type="hidden" name="announcement-type">
                        <select class="form-select" aria-label="Default select example" v-model="type_select" :disabled="selectedItem">
                            <option value="" disabled hidden selected>Select Type</option>
                            <option value="election">Election</option>
                            <option value="debate">Debate</option>
                            <option value="open-forum">Open Forum</option>
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
                        <input class="form-control" type="id" name="id" v-model="count_input" :disabled="true">
                    </div>
                </div>

                <div>
                    <div class="form-group">
                        <label for="body" class="form-label">Body</label>
                        <textarea class="form-control body" type="text" name="selected-body" v-model="body_input"></textarea>
                    </div>
                </div>

                <div class="row">
                    <h6 class="section-title">Attachments</h6>
                        <div class="form-group col-2">
                            <label class="form-label" for="selected">Type of Attachment</label>
                            <input type="hidden" name="attachment-type">
                            <select class="form-select" aria-label="Default select example" v-model="type_of_attachment" :disabled="is_loading_attachments">
                                <option value="None" selected>None</option>
                                <option value="Banner">Banner</option>
                                <option value="Poster">Poster</option>
                            </select>

                            <div v-if="type_of_attachment !== 'None'">
                                <label for="file-upload" class="custom-file-upload">
                                    Select File
                                </label>
                                <input id="file-upload" type="file" style="display: none;" @change="onFileChange" multiple/>
                            </div>
                        </div>

                    <div class="form-group col-4">
                        <DragAndDrop 
                            v-if="type_of_attachment !== 'None'" 
                            v-model="upload_image_attachments" 
                            :acceptedFileTypes="'image/'" 
                            :isLoadingAttachments="is_loading_attachments">
                        </DragAndDrop>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <button class="delete-btn" :disabled="!selectedItem">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <ActionButton @submit.prevent="save" class="save-btn" :disabled="saving">{{ SaveButtonText }}</ActionButton>
                    </div>
                </div>
            </form>
        </BaseContainer>

        <BaseContainer class="item-container" :height="'335px'">
            <BaseTable class="item-table" :columns="['ID', 'Type', 'Title']" :table-height="'235px'">
                <tr v-for="(item, index) in items" :key="index" @click="selectItem(item)" 
                    v-bind:class="{ 'active-row': selectedItem && selectedItem.id === item.id && selectedItem.announcement_type === item.announcement_type }">
                    <td class="my-cell">{{ item.count }}</td>
                    <td class="my-cell">{{ item.announcement_type.charAt(0).toUpperCase() + item.announcement_type.slice(1) }}</td>
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
import DragAndDrop from '../../Shared/DragAndDrop.vue';

import axios from 'axios';
import { ref } from 'vue';


export default {
    setup() {
        const type_select = ref('');
        const title_input = ref('');
        const id_input = ref('');
        const count_input = ref('');
        const body_input = ref('');
        const type_of_attachment = ref('None');
        const upload_image_attachments = ref([]);
        
        // States
        const selectedItem = ref(null);
        const new_button_disabled = ref(true);
        const saving = ref(false);
        const is_loading_attachments = ref(false);

        // Data for the table
        const items = ref([]);

        return {
            type_select,
            title_input,
            id_input,
            count_input,
            body_input,
            type_of_attachment,
            upload_image_attachments,
            selectedItem,
            new_button_disabled,
            saving,
            is_loading_attachments,
            items,
        }
    },
    components: { Navbar, Sidebar, BaseTable, BaseContainer, ActionButton, DragAndDrop },
    created() {
        this.getLatestAnnouncementCount();
        this.fetchTableData();
    },
    computed: {
        SaveButtonText() {
            if (this.saving) {
                return 'Saving...';
            }
            else{
                if (this.selectedItem) {
                    return 'Update';
                }
                else {
                    return 'Save';
                }
            }
        }
    },
    methods: {
        fetchTableData() {
            axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/all`)
                .then(response => {
                    const announcements = response.data.announcements.map(item => {
                        return {
                            id: item.AnnouncementId,
                            count: "Announcement #" + item.count,
                            announcement_type: item.AnnouncementType,
                            title: item.AnnouncementTitle,
                            body: item.AnnouncementBody,
                            attachment_type: item.AttachmentType,
                        }
                    });

                    this.items = [...announcements];
                })
                .catch(error => {
                    console.log(error);
                });
        },
        reset() {
            // Reset the selected row item to null
            this.selectedItem = null;

            // Reset the input fields
            this.type_select = '';
            this.title_input = '';
            this.id_input = '';
            this.getLatestAnnouncementCount();
            this.body_input = '';
            this.type_of_attachment = 'None';
            this.upload_image_attachments = [];

            this.new_button_disabled = true;
        },
        newButtonSelected() {
            this.reset();
        },
        getLatestAnnouncementCount() {
            axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/count/latest`)
            .then(response => {
                this.count_input = "Announcement #" + (response.data.count + 1);
            })
            .catch(error => {
                console.log(error);
            });
        },
        addFiles(files) {
            // Add the files to the list of files
            for (let i = 0; i < files.length; i++) {
                let file = files[i];

                // Since we are only accepting images (banner or poster), check if a file is an image or not
                if (!file.type.startsWith('image/')) {
                    alert(file.name + ' is not an image, please upload an image file');
                    continue;  
                }

                // Check if the file is already in the list of files
                // If it is, then do not add it again
                if (!this.upload_image_attachments.some(existingFile => existingFile.name === file.name)) {
                    this.upload_image_attachments.push(file);
                }
            }
        },
        onFileChange(event) {
            this.addFiles(event.target.files);
        },
        selectItem(item) {
            // If currently loading the attachments, do not allow selecting a row
            if (this.is_loading_attachments) {
                return;
            }

            // When a row is selected
            this.selectedItem = item;
            this.new_button_disabled = false; // Enable the new button since a row is selected

            // Set the input fields to the selected row item
            this.type_select = item.announcement_type;
            this.title_input = item.title;
            this.id_input = item.id; 
            this.count_input = item.count;
            this.body_input = item.body;
            this.type_of_attachment = item.attachment_type;

            this.is_loading_attachments = true;

            // Fetch the files for the selected item
            axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/get/attachment/${item.id}`)
                .then(response => {
                    // Clear the list of files first
                    this.upload_image_attachments = [];

                    this.upload_image_attachments = response.data.files.map(file => ({
                        id: file.id,
                        name: file.name,
                        size: file.size,
                        createdDateTime: file.createdDateTime,
                        lastModifiedDateTime: file.lastModifiedDateTime,
                        downloadUrl: file.downloadUrl,
                    }));
                    console.log(response.duration);
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => {
                    this.is_loading_attachments = false;
                });
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

            // If selected a type of attachment (banner or poster)
            if (this.type_of_attachment !== 'None') {

                // If there are no image attachment uploaded but selected a type of attachment
                if (this.upload_image_attachments.length < 1) {
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

            // Append the image attachments to the FormData object if there are any image attachments
            if (this.type_of_attachment !== 'None' && this.upload_image_attachments.length > 0) {
                for (let i = 0; i < this.upload_image_attachments.length; i++) {
                    formData.append('attachment_images', this.upload_image_attachments[i]);
                }
            }

            // If validation passed, check if can update
            if (this.saving === true) {
                return;
            }
            
            // Saving state is true
            this.saving = true;

            axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/save`, formData, {
                })
                .then(response => {
                    console.log(response.duration);
                    alert('Announcement saved successfully')

                    this.reset();
                })
                .catch(error => {
                    console.error(error);
                })
                .finally(() => {
                    this.saving = false;
                    this.fetchTableData();
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

.custom-file-upload {
    margin-top: 7%;
    padding: 7px;
    width: 100%;
    font-size: 100%;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    cursor: pointer;
    text-align: center;
}

.custom-file-upload:hover{
    background-color: #f4f4f4;
}

#dropzone {
    width: 100%;
    height: 200px;
    background-color: #e0e0e0;
    border-radius: 10px;
}

.drag-drop-default-container{
    display: flex;
    flex-direction: column; /* Stacks items vertically */
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 100%; 
    width: 100%;
}

.drag-drop-files-container{
    display: grid;
    align-content: start;
    justify-items: start;
    
    max-height: 200px; 
    height: 100%;
    width: 100%;

    overflow-y: auto; 
    overflow-x: hidden;
}

.file-list {
    display: flex;
    justify-content: space-between;
    width: 100%;

    margin-top: 2%;
    margin-left: 3%;
}

.file-list span {
    word-wrap: break-word; 
    width: 90%; 
}


.remove-attachment{
    background-color: #B90321;
    color: white;
    width: 30px;
    border-radius: 8px;
    outline: none;
    border: none;
}

.save {
    text-align: right;
}

.save-btn{
    margin-top: 1.5%;
}

.save-btn:disabled{
    background-color: #cccccc;
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

.delete-btn:disabled{
    color: #cccccc;
}

.head {
    text-align: center;
}

.section-title {
    font-weight: bolder;
    margin-top: 1%;
}

.item-container{
    margin-bottom: 2%;
}
</style>