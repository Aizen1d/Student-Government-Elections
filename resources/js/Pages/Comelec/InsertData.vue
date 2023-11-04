<template>
    <title>Insert Data - EMS</title>
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
                                <input class="form-control margin" type="text" maxlength="15" name="stud-num" v-model="student_number">
                            </div>
                            <div class="col">
                                <label class="form-label" for="course">Course</label>
                                <input type="hidden" name="course">
                                <select class="form-select" aria-label="Default select example" v-model="course">
                                    <option value="" disabled hidden selected>Select</option>
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
                        <input class="form-control margin" type="text" name="f-name" v-model="first_name">
                        
                        <label class="form-label" for="m-name">Middle Name</label>
                        <input class="form-control margin" type="text" name="m-name" v-model="middle_name">

                        <label class="form-label" for="l-name">Last Name</label>
                        <input class="form-control margin" type="text" name="l-name" v-model="last_name">

                        <div class="row">
                            <div class="col">
                                <label class="form-label" for="email">Email Address</label>
                                <input class="form-control margin mb-3" type="email" name="email" v-model="email">

                                <label class="form-label" for="sem">Current Semester</label>
                                <select class="form-select margin" name="sem" v-model="semester" aria-label="Default select example">
                                    <option value="" disabled hidden selected>Select semester</option>
                                    <option value="1st Semester">1st Semester</option>
                                    <option value="2nd Semester">2nd Semester</option>
                                </select>
                            </div>
                            <div class="col">
                                <label class="form-label" for="bday">Birth Date</label>
                                <input class="form-control margin mb-3" type="date" name="bday" v-model="birth_date">

                                <label class="form-label" for="year">Year Enrolled</label>
                                <select class="form-select margin" name="SY" v-model="year_enrolled">
                                    <option value="" disabled hidden selected>Select year enrolled</option>
                                    <option v-for="year in validYears" :key="year" :value="year">{{ year }}</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <div class="row mt-3">
                                <div class="col">
                                    <ActionButton class="clear" @click.prevent="clearAll">Clear All</ActionButton>
                                </div>
                                <div class="col">
                                    <ActionButton class="insert" @click.prevent="manualInsert">Insert</ActionButton>
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

                        <ActionButton @click.prevent="submitAttachmentFile" :disabled="saving" class="mt-4 upload">Upload file</ActionButton>
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
            const student_number = ref('');
            const course = ref('');
            const first_name = ref('');
            const middle_name = ref('');
            const last_name = ref('');
            const email = ref('');
            const birth_date = ref('');
            const semester = ref('');
            const year_enrolled = ref('');

            const selectedFiles = ref([]);
            const file_size = ref(10); // mega bytes
            const saving = ref(false);
            const updating = ref(false);
            const is_loading_attachments = ref(false);
            const notAcceptedMessage = ref('please upload a csv/excel file.');
            const extensions = ref('application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv') 

            return {
                student_number,
                course,
                first_name,
                middle_name,
                last_name,
                email,
                birth_date,
                semester,
                year_enrolled,
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
        computed:{
            validYears() {
                return this.getYears();
            },
        },
        methods: {
            getYears() {
                const startYear = 2020;
                const endYear = new Date().getFullYear() + 2;
                return Array.from({length: endYear - startYear}, (_, i) => startYear + i);
            },
            clearAll() {
                this.student_number = '';
                this.course = '';
                this.first_name = '';
                this.middle_name = '';
                this.last_name = '';
                this.email = '';
                this.birth_date = null;
                this.semester = '';
                this.year_enrolled = '';
            },
            manualInsert() {
                if (this.student_number == '') {
                    alert('Please enter a student number.');
                    return;
                }
                if (this.course == '') {
                    alert('Please select a course.');
                    return;
                }
                if (this.first_name == '') {
                    alert('Please enter a first name.');
                    return;
                }
                if (this.last_name == '') {
                    alert('Please enter a last name.');
                    return;
                }
                if (this.email == '') {
                    alert('Please enter an email address.');
                    return;
                }
                if (this.birth_date == null || this.birth_date == '') {
                    alert('Please enter a birth date.');
                    return;
                }
                if (this.semester == '') {
                    alert('Please select a semester.');
                    return;
                }
                if (this.year_enrolled == '') {
                    alert('Please select a year enrolled.');
                    return;
                }

                this.saving = true;

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/insert/data/manual`, {
                    student_number: this.student_number,
                    course: this.course,
                    first_name: this.first_name,
                    middle_name: this.middle_name,
                    last_name: this.last_name,
                    email: this.email,
                    birth_date: this.birth_date,
                    semester: this.semester,
                    year_enrolled: String(this.year_enrolled),
                })
                .then(response => {
                    if (response.data.error) {
                        alert(response.data.error);
                    } 
                    else {
                        console.log(`Student successfully inserted. Duration: ${response.duration}`)
                        alert(response.data.message);
                        this.clearAll();
                    }
                }).catch(error => {
                    console.log(error);
                })
                .finally(() => {
                    this.saving = false;
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
                if (this.selectedFiles.length == 0) {
                    alert('Please select a file to upload.');
                    return;
                }

                let formData = new FormData();

                for (let i = 0; i < this.selectedFiles.length; i++) {
                    formData.append('files', this.selectedFiles[i].file);
                }

                this.saving = true;

                axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/insert/data/attachment`, formData, {
                    })
                .then(response => {
                    response.data.responses.forEach(fileResponse => {
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

                    // Open the PDF in a new tab
                    if (response.data.pdf_url) {
                        window.open(response.data.pdf_url);
                    }
                }).catch(error => {
                    console.log(error);
                })
                .finally(() => {
                    this.saving = false;
                    this.selectedFiles = [];
                });
            },
        }
    }
</script>

<style scoped>
.components{
    margin-left: 17.3%;
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

.upload:disabled{
    background-color: #cccccc;
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