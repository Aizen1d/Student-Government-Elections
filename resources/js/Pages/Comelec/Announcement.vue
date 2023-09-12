<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Announcements</h2>
            </div>
            <div class="col-6 new">
                <button :disabled="new_button_disabled" class="new-btn">New Announcement</button>
            </div>
        </div>

        <div class="mainbox">
            <form @submit.prevent="save">
                <div class="form-group row">
                    <div class="col-2">
                        <label class="form-label" for="selected">Type of Announcement</label>
                        <input type="hidden" name="announcement-type">
                        <select class="form-select" aria-label="Default select example" v-model="type_select">
                            <option value="" disabled hidden selected>Select Type</option>
                            <option value="1">Election</option>
                            <option value="2">Debate</option>
                            <option value="3">Open Forum</option>
                            <option value="4">Educational Program</option>
                            <option value="5">Results</option>
                        </select>
                    </div>
                    <div class="col-8">
                        <label class="form-label" for="title">Title</label>
                        <input class="form-control" type="title" name="title" v-model="title_input">
                    </div>
                    <div class="col-2">
                        <label class="form-label" for="id">ID</label>
                        <input class="form-control" type="id" name="id" v-model="id_input" readonly>
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
                        <input type="file" name="attachment" class="form-control" ref="fileInput" @change="onFileChange">                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <button class="delete-btn">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <button @submit.prevent="save" class="new-btn">Save</button>
                    </div>
                </div>
            </form>
        </div>

        <div class="list">
            <table class="table table-hover table-bordered border-dark table-responsive">
                <thead class="head">
                    <tr>
                        <th>#</th>
                        <th class="th-sm">Type</th>
                        <th class="th-sm">Title</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                       
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import Navbar from '../../Shared/Navbar.vue';
import Sidebar from '../../Shared/Sidebar.vue';

import axios from 'axios';
import { ref } from 'vue';


export default {
    setup() {
        const type_select = ref('');
        const title_input = ref('');
        const id_input = ref('');
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
            body_input,
            type_of_attachment,
            upload_image_attachment,
            fileInput,
            new_button_disabled,
            saving,
            items,
        }
    },
    components: { Navbar, Sidebar },
    created() {
        axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/announcement/id/latest`)
            .then(response => {
                this.id_input = "Announcement #" + (response.data.id + 1);
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
                if (this.upload_image_attachment) {
                    return alert('Please attach your image');
                }
            }
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

.new {
    margin-top: -1%;
    text-align: end;
}

.new-btn {
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 100px 15px 100px;
    border: transparent;
    border-radius: 10px;
    background-color: #B90321;
    color: white;
}

.new-btn:disabled {
    background-color: #cccccc;
}

.mainbox,
.list {
    margin-top: 1.5%;
    background-color: white;
    margin: 1.5% -1% 0% -1%;
    padding: 30px 30px 20px 30px;
    border-radius: 7px;
}

.body {
    resize: none;
    overflow-y: auto;
    height: 200px;
}

.form-group {
    padding-bottom: 15px;
}

.save {
    text-align: right;
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

.head {
    text-align: center;
}

.section-title {
    font-weight: bolder;
    margin-top: 1%;
}</style>