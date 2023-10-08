<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components mb-4">
        <h2>Insert Data</h2>
        
        <form action="">
            <div class="row g-4">
                <div class="col-6">
                    <div class="note">
                        <h6>Manually input student data.</h6>
                    </div>
                    <div class="box">
                        <div class="row mb-2">
                            <div class="col">
                                <label class="form-label" for="stud-num">Student Number</label>
                                <input class="form-control margin" type="text" name="stud-num">
                            </div>
                            <div class="col">
                                <label class="form-label" for="course">Course</label>
                                <input type="hidden" name="course">
                                <select class="form-select" aria-label="Default select example">
                                    <option disabled hidden selected>Select</option>
                                    <option value="1">BBTLEDHE</option>
                                    <option value="2">BSBAHRM</option>
                                    <option value="3">BSBA-MM</option>
                                    <option value="4">BSENTREP</option>
                                    <option value="5">BSIT</option>
                                    <option value="6">BPAPFM</option>
                                    <option value="7">DOMTMOM</option>
                                </select>
                            </div>
                        </div>
                        <label class="form-label" for="f-name">First Name</label>
                        <input class="form-control margin" type="text" name="f-name">
                        
                        <label class="form-label" for="m-name">Middle Name</label>
                        <input class="form-control margin" type="text" name="m-name">

                        <label class="form-label" for="l-name">Last Name</label>
                        <input class="form-control margin" type="text" name="l-name">

                        <div class="row">
                            <div class="col">
                                <label class="form-label" for="email">Email Address</label>
                                <input class="form-control margin mb-3" type="email" name="email">

                                <label class="form-label" for="sem">Current Semester</label>
                                <input class="form-control margin" type="text" name="sem">
                            </div>
                            <div class="col">
                                <label class="form-label" for="bday">Birth Date</label>
                                <input class="form-control margin mb-3" type="date" name="bday">

                                <label class="form-label" for="year">Year Enrolled</label>
                                <input class="form-control margin" type="text" name="year">
                            </div>
                        </div>

                        <div>
                            <div class="row mt-3">
                                <div class="col">
                                    <ActionButton class="clear">Clear All</ActionButton>
                                </div>
                                <div class="col">
                                    <ActionButton class="insert">Insert</ActionButton>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-6">
                    <div class="note">
                        <h6>Upload CSV/Excel files.</h6>
                    </div>
                    <div class="box">
                        <label for="file-upload" class="custom-file-upload" :class="{ 'disabled': is_loading_attachments || saving || updating }">
                                    Select File
                        </label>
                        <input id="file-upload" type="file" style="display: none;" @change="onFileChange" :disabled="is_loading_attachments || saving || updating" multiple/>

                        <DragAndDrop 
                            class="drag-and-drop"
                            v-model="selectedFiles" 
                            :fileSize="file_size"
                            :acceptedFileTypes="extensions"
                            :notAcceptedMessage="notAcceptedMessage"
                            :isLoadingAttachments="is_loading_attachments"
                            :saving="saving"
                            :updating="updating">
                        </DragAndDrop>

                        <ActionButton @click.prevent="submitAttachmentFile" class="mt-4 upload">Upload file</ActionButton>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script >
    import { useUserStore } from '../../Stores/UserStore';
    import { router } from '@inertiajs/vue3'
    import { ref } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import SearchBarAndFilter from '../../Shared/SearchBarAndFilter.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import DragAndDrop from '../../Shared/DragAndDrop.vue';

    import axios from 'axios';

    export default {
        setup() {
            const selectedFiles = ref([]);
            const file_size = ref(10); // mega bytes
            const saving = ref(false);
            const updating = ref(false);
            const is_loading_attachments = ref(false);
            const notAcceptedMessage = ref('please upload a csv/excel file.');
            const extensions = ref('application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv') 

            return {
                selectedFiles,
                file_size,
                saving,
                updating,
                is_loading_attachments,
                notAcceptedMessage,
                extensions,
            }
        },
        components: { Navbar, Sidebar, ActionButton, SearchBarAndFilter, BaseContainer, BaseTable, DragAndDrop },
        methods: {
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
                    if (!this.selectedFiles.some(existingFile => existingFile.name === file.name)) {
                        this.selectedFiles.push({ file:file, 
                                                name: file.name, 
                                                url: url
                                            });
                    }
                }
            },
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files;

                if (files) {
                    this.addFiles(files);
                }

                // Clear the input value
                e.target.value = null;
            },
            submitAttachmentFile() {
                let formData = new FormData();

                for (let i = 0; i < this.selectedFiles.length; i++) {
                    formData.append('files', this.selectedFiles[i].file);
                }

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/insert/data`, formData, {
                }).then(response => {
                    response.data.forEach(fileResponse => {
                        if (fileResponse.unexpected_columns) {
                            alert(`File: ${fileResponse.file}, Message: ${fileResponse.unexpected_columns.message}`);
                        } 
                        else if (fileResponse.no_new_students) {
                            alert(fileResponse.no_new_students)
                        }
                        else {
                            console.log(`File successfully uploaded. Duration: ${response.duration}`)
                            alert(`File: ${fileResponse.file}, Message: ${fileResponse.message}`);
                        }
                    });
                }).catch(error => {
                    console.log(error);
                });
            },
        }
    }
</script>

<style scoped>
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

.margin{
    margin-bottom: 2%;
    margin-left: 0%;
}

.note{
    margin-top: 1.5%;
    background-color: #FDD5D5;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    padding: 2%;
}

.note h6{
    margin-top: 10px;
}

.box{
    background-color: white;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    padding: 3%;
}

.clear{
    width: 100%;
}

.insert{
    width: 100%;
}

.upload{
    width: 100%;
}

.custom-file-upload {
    margin-bottom: 2.5%;
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

.drag-and-drop{
    height: 250px;
}
</style>