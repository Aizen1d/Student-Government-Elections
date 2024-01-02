<template>
    <title>Announcements - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Announcements</h2>
            </div>
            <div class="col-6 new">
                <ActionButton :disabled="new_button_disabled || saving || updating || is_loading_attachments" class="new-btn" @click="newButtonSelected">New Announcement</ActionButton>
            </div>
        </div>

        <BaseContainer :height="'auto'" :maxHeight="'800px'">
            <form @submit.prevent="save">
                <div class="form-group row">
                    <div class="col-2">
                        <label class="form-label" for="selected">Type of Announcement</label>
                        <input type="hidden" name="announcement-type">
                        <select class="form-select" aria-label="Default select example" v-model="type_select" :disabled="selectedItem || saving || updating">
                            <option value="" disabled hidden selected>Select Type</option>
                            <option value="elections">Elections</option>
                            <option value="debates">Debates</option>
                            <option value="open-forums">Open Forums</option>
                            <option value="educational-programs">Educational Programs</option>
                            <option value="results">Results</option>
                        </select>
                    </div>
                    <div class="col-8">
                        <label class="form-label" for="title">Title</label>
                        <input class="form-control" type="title" name="title" v-model="title_input" :disabled="saving || updating">
                    </div>
                    <div class="col-2">
                        <label class="form-label" for="id">ID</label>
                        <input class="form-control" type="id" name="id" v-model="count_input" :disabled="true">
                    </div>
                </div>

                <div>
                    <div class="form-group">
                        <label for="body" class="form-label">Body</label>
                        <textarea class="form-control body" type="text" name="selected-body" v-model="body_input" :disabled="saving || updating"></textarea>
                    </div>
                </div>

                <div class="row">
                    <h6 class="section-title">Attachments</h6>
                        <div class="form-group col-2">
                            <label class="form-label" for="selected">Type of Attachment</label>
                            <input type="hidden" name="attachment-type">
                            <select class="form-select" aria-label="Default select example" v-model="type_of_attachment" :disabled="is_loading_attachments || saving || updating">
                                <option value="None" selected>None</option>
                                <option value="Banner">Banner</option>
                                <option value="Poster">Poster</option>
                            </select>

                            <div v-if="type_of_attachment !== 'None'">
                                <label for="file-upload" class="custom-file-upload" :class="{ 'disabled': is_loading_attachments || saving || updating }">
                                    Select File
                                </label>
                                <input id="file-upload" type="file" style="display: none;" @change="onFileChange" :disabled="is_loading_attachments || saving || updating" multiple/>
                            </div>
                        </div>

                    <div class="form-group col-4">
                        <DragAndDrop 
                            v-if="type_of_attachment !== 'None'" 
                            v-model="upload_image_attachments" 
                            :fileSize="file_size"
                            :acceptedFileTypes="extensions"
                            :notAcceptedMessage="notAcceptedMessage"
                            :isLoadingAttachments="is_loading_attachments"
                            :saving="saving"
                            :updating="updating">
                        </DragAndDrop>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <button class="delete-btn" :disabled="!selectedItem || is_loading_attachments || updating" @click.prevent="deleteItem">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <ActionButton @submit.prevent="save" class="save-btn" :disabled="saving || updating || is_loading_attachments">{{ SaveButtonText }}</ActionButton>
                    </div>
                </div>
            </form>
        </BaseContainer>

        <BaseContainer class="item-container" :height="'auto'" :maxHeight="'500px'">
            <BaseTable class="item-table" 
                    :columns="['ID', 'Type', 'Title']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'280px'">
                <tr v-for="(item, index) in announcementData" v-if="isAnnouncementSuccess" :key="index" @click="selectItem(item)" 
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
import { ref, watch, watchEffect, computed } from 'vue';

import { useQuery, useMutation, useQueryClient  } from "@tanstack/vue-query";

export default {
    setup() {
        const type_select = ref('');
        const title_input = ref('');
        const id_input = ref('');
        const count_input = ref('');
        const body_input = ref('');
        const type_of_attachment = ref('None');
        const upload_image_attachments = ref([]);
        const retrieved_attachments = ref([]);
        const file_size = ref(5); // mega bytes
        const notAcceptedMessage = ref('please upload an image only.');
        const extensions = ref('image/jpeg,image/png,image/gif,image/bmp')
        
        // States
        const selectedItem = ref(null);
        const new_button_disabled = ref(true);
        const saving = ref(false);
        const updating = ref(false);
        const is_loading_attachments = ref(false);

        // Data for the table
        const items = ref([]);

        const queryClient = new useQueryClient();

        const fetchAnnouncementTable = async () => {
            const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/all`);

            return response.data.announcements.map(item => {
                return {
                    id: item.AnnouncementId,
                    count: "Announcement #" + item.count,
                    announcement_type: item.AnnouncementType,
                    title: item.AnnouncementTitle,
                    body: item.AnnouncementBody,
                    attachment_type: item.AttachmentType,
                }
            });
        }

        const { data: announcementData, 
                isLoading: isAnnouncementLoading, 
                isSuccess: isAnnouncementSuccess, 
                isError: isAnnouncementError } = 
                useQuery({
                    queryKey: ['fetchAnnouncement'],
                    queryFn: fetchAnnouncementTable,
                    refetchInterval: 1000,
                });

        return {
            type_select,
            title_input,
            id_input,
            count_input,
            body_input,
            type_of_attachment,
            upload_image_attachments,
            retrieved_attachments,
            file_size,
            notAcceptedMessage,
            extensions,

            selectedItem,
            new_button_disabled,
            saving,
            updating,
            is_loading_attachments,
            items,

            fetchAnnouncementTable,
            announcementData,
            isAnnouncementLoading,
            isAnnouncementSuccess,
            isAnnouncementError,
        }
    },
    components: { Navbar, Sidebar, BaseTable, BaseContainer, ActionButton, DragAndDrop },
    computed: {
        SaveButtonText() {
            if (this.saving) {
                return 'Saving...';
            }
            else{
                if (this.selectedItem) {
                    if (this.updating) {
                        return 'Updating...';
                    }   
                    else {
                        return 'Update';
                    }
                }
                else {
                    return 'Save';
                }
            }
        }
    },
    created() {
        this.getLatestAnnouncementCount();
    },
    methods: {
        fetchTableData() {
            axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/all`)
                .then(response => {
                    console.log(`Announcement table data fetched successfully. Duration: ${response.duration}ms`)
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
                console.log(`Latest announcement count fetched successfully. Duration: ${response.duration}ms`)
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

                if (file.size > this.file_size * 1024 * 1024) {
                    alert(file.name + ' is larger than ' + String(this.file_size) + ' MB, please upload a smaller file');
                    continue;
                }

                const extensions = this.extensions;
                let acceptedTypes = extensions.split(',');

                if (!acceptedTypes.includes(file.type)) {
                    alert(file.name + ' is not an accepted file type, ' + this.notAcceptedMessage);
                    continue;
                }

                // Create a new object URL for the file
                let url = URL.createObjectURL(file);

                // Check if the file is already in the list of files
                // If it is, then do not add it again
                if (!this.upload_image_attachments.some(existingFile => existingFile.name === file.name)) {
                    this.upload_image_attachments.push({file: file, 
                                                        name: file.name,
                                                        url: url
                                                    });
                }
            }
        },
        onFileChange(e) {
            let files = e.target.files;

            if (files) {
                this.addFiles(files);
            }

            // Clear the input value
            e.target.value = null;
        },
        selectItem(item) {
            if (item === this.selectedItem) {
                return;
            }

            // If currently loading the attachments, do not allow selecting a row
            if (this.is_loading_attachments) {
                alert('Cannot select a row while loading attachments');
                return;
            }
            if (this.saving || this.updating) {
                alert('Cannot select a row while saving or updating');
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
                    console.log(`Announcement attachments fetched successfully. Duration: ${response.duration}ms`)

                    // Clear the list of files first
                    this.upload_image_attachments = [];

                    // Push the retrieved files to the upload_image_attachments array
                    response.data.images.forEach(retrieved_file => {
                        let file = new File([], retrieved_file.name);
                        this.upload_image_attachments.push({
                                                            file: file, 
                                                            name: file.name,
                                                            url: retrieved_file.url
                                                        });

                    
                    });
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => {
                    this.retrieved_attachments = [...this.upload_image_attachments];
                    this.is_loading_attachments = false;
                });
        },
        deleteItem() {
            // Delete the selected row item
            if (this.selectedItem === null) {
                return alert('Please select an item to delete');
            }

            const confirmDelete = confirm('Are you sure you want to delete this item?');
            if (!confirmDelete) {
                return;
            }
            
            let id = this.selectedItem.id;

            axios.delete(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/delete`, {
                data: { id: id }
            })
            .then(response => {
                console.log(`Announcement with id ${id} was deleted successfully. Duration: ${response.duration}ms`)
                alert('Item deleted successfully');
            })
            .catch(error => {
                console.error(error);
            })
            .finally(() => {
                //this.fetchAnnouncementTable();
                this.fetchTableData();
                this.reset();
            })
        },
        save() {
            // If selected a row item (updating state), update instead
            if (this.selectedItem) {
                return this.update();
            }

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
                    formData.append('attachment_images', this.upload_image_attachments[i].file);
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
                    console.log(`Announcement saved successfully. Duration: ${response.duration}ms`)
                    alert('Announcement saved successfully')

                    this.reset();
                })
                .catch(error => {
                    console.error(error);
                })
                .finally(() => {
                    this.saving = false;
                    //this.fetchAnnouncementTable();
                    this.fetchTableData();
                });
        },
        update() {
            // If validation passed, check if can update
            if (this.updating === true) {
                return;
            }
            
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
            let attachments_modified = false;
            let new_files = [];
            let removed_files = [];

            // Append the form fields to the FormData object
            formData.append('id_input', this.id_input);
            formData.append('type_select', this.type_select);
            formData.append('title_input', this.title_input);
            formData.append('body_input', this.body_input);
            formData.append('type_of_attachment', this.type_of_attachment);

            // Check if the attachments were modified
            if (this.upload_image_attachments.length !== this.retrieved_attachments.length) {
                attachments_modified = true;
            } 
            else {
                for (let i = 0; i < this.upload_image_attachments.length; i++) {
                    if (this.upload_image_attachments[i] !== this.retrieved_attachments[i]) {
                        attachments_modified = true;
                        break;
                    }
                }
            }

            // To improve performance, if not modified, just look for db updates directly
            if (attachments_modified) {
                formData.append('attachments_modified', 'true');
                
                // Check for new files
                for (let i = 0; i < this.upload_image_attachments.length; i++) {
                    if (!this.retrieved_attachments.includes(this.upload_image_attachments[i])) {
                        new_files.push(this.upload_image_attachments[i].file);
                    }
                }

                // Check for removed files
                for (let i = 0; i < this.retrieved_attachments.length; i++) {
                    if (!this.upload_image_attachments.includes(this.retrieved_attachments[i])) {
                        removed_files.push(this.retrieved_attachments[i]);
                    }
                }

                // Append new files
                for (let i = 0; i < new_files.length; i++) {
                    formData.append('new_files', new_files[i]);
                }

                // Append removed files
                for (let i = 0; i < removed_files.length; i++) {
                    formData.append('removed_files', removed_files[i].file);
                }
            } 
            else {
                formData.append('attachments_modified', 'false');
            }

            // Append the image attachments to the FormData object if there are any image attachments
            if (this.type_of_attachment !== 'None' && this.upload_image_attachments.length > 0) {
                for (let i = 0; i < this.upload_image_attachments.length; i++) {
                    formData.append('attachment_images', this.upload_image_attachments[i].file);
                }
            }

            // Updating state is true
            this.updating = true;

            axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/update`, formData, {
                })
                .then(response => {
                    console.log(`Announcement updated successfully. Duration: ${response.duration}ms`);
                    this.retrieved_attachments = [...this.upload_image_attachments];
                                                    
                    alert('Announcement updated successfully')
                })
                .catch(error => {
                    console.error(error);
                })
                .finally(() => {
                    this.updating = false;
                    //this.fetchAnnouncementTable();
                    this.fetchTableData();
                });
        },
    },
}

</script>

<style scoped>
.components {
    margin-left: 18%;
    margin-top: 2%;
    font-family: 'Inter', sans-serif;
    margin-right: 3.2%;
}

.components h2 {
    font-weight: 800;
    font-size: 30px;
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

.custom-file-upload.disabled {
    background-color: #E9ECEF;
    cursor: default;
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
    margin-top: 1%;
}

.item-container{
    margin-bottom: 2.5%;
}
</style>