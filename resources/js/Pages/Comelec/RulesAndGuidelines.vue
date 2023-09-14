<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Rules & Guidelines</h2>
            </div>
            <div class="col-6 new">
                <button :disabled="new_button_disabled" @click="newButtonSelected" class="new-btn">New</button>
            </div>      
        </div>   
        
        <div class="mainbox">
            <form @submit.prevent="save">
                <div class="form-group row">
                    <div class="col-2">
                        <label class="form-label" for="selected">Type</label>
                        <input class="input-outline" type="hidden" name="colors-product">
                        <select class="form-select" aria-label="Default select example" v-model="type_select" :disabled="selectedItem">
                            <option value="" disabled hidden selected>Select Type</option>
                            <option value="rule">Rule</option>
                            <option value="guideline">Guideline</option>
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
                    <div class="col-6">
                        <button class="delete-btn" @click.prevent="deleteItem">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <button @submit.prevent="save" class="save-btn">{{ saveButtonText }}</button>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="list">
            <table class="my-table table-responsive">
                <thead class="my-thead head">
                    <tr>
                        <th class="my-cell">ID</th>
                        <th class="my-cell th-sm">Type</th>
                        <th class="my-cell th-sm">Title</th>
                    </tr>
                </thead>
                <tbody class="my-tbody">
                    <tr v-for="(item, index) in items" :key="index" @click="selectItem(item)" 
                        :class="{ 'active-row': selectedItem && selectedItem.id === item.id }">
                        <td class="my-cell">{{ item.count }}</td>
                        <td class="my-cell">{{ item.type.charAt(0).toUpperCase() + item.type.slice(1) }}</td>
                        <td class="my-cell">{{ item.title }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import { Link } from '@inertiajs/vue3'
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';

    import axios from 'axios';
    import { ref, watch } from 'vue';

    export default {
        setup() {
            const type_select = ref('');
            const title_input = ref('');
            const id_input = ref('');
            const count_input = ref('');
            const body_input = ref('');

            const can_save = ref(true);
            
            const new_button_disabled = ref(true); 
            const selectedItem = ref(null);
            const items = ref([]);

            // Updates the value of the count_input element for rule/guideline creation
            // import.meta.env.VITE_FASTAPI_BASE_URL is the dynamic base URL of the FastAPI server
            const updateIdInput = (prefix, endpoint) => () => {
                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}${endpoint}`)
                    .then(response => {
                        console.log(response.duration); // Log the response time
                        const data = response.data;

                        if (data.id === 0) {
                            count_input.value = prefix + 1;
                        }
                        else {
                            count_input.value = prefix + (data.id + 1);
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    });
            };

            // Watch type_select(rule/guideline) for changes
            watch(type_select, (newValue) => {
                // Only update count_input.value if no row is selected
                if (!selectedItem.value) {
                    if (newValue === 'rule') {
                        updateIdInput('Rule #', '/api/v1/rule/id/latest')();
                    }
                    else if (newValue === 'guideline') {
                        updateIdInput('Guideline #', '/api/v1/guideline/id/latest')();
                    }
                }
            });
            
            return {
                type_select, 
                title_input,
                id_input,
                count_input,
                body_input,
                new_button_disabled,
                selectedItem,
                items,
                can_save,
            }
        },
        created() {
            this.fetchTableData();
        },
        computed: {
            saveButtonText() {
                return this.selectedItem ? 'Update' : 'Save';
            }
        },
        components: { Link, Navbar, Sidebar },
        methods: {
            newButtonSelected() {
                // Reset the selected row item to null
                this.selectedItem = null;

                // Reset the input fields
                this.type_select = '';
                this.title_input = '';
                this.id_input = '';
                this.count_input = '';
                this.body_input = '';

                // Disable the new button since no row is selected
                this.new_button_disabled = true;
            },
            selectItem(item) {
                // When a row is selected
                this.selectedItem = item;
                this.new_button_disabled = false; // Enable the new button since a row is selected

                // Set the input fields to the selected row item
                this.type_select = item.type;
                this.title_input = item.title;
                this.id_input = item.id; 
                this.count_input = item.count;
                this.body_input = item.body;
            },
            deleteItem() {
                // Delete the selected row item
                if (this.selectedItem === null) {
                    return alert('Please select an item to delete');
                }
                
                let id = this.selectedItem.id;
                let type = this.selectedItem.type;

                axios.delete(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/${type}/delete`, {
                    data: { id: id }
                })
                .then(response => {
                    console.log(response.data);
                    alert('Item deleted successfully');
                })
                .catch(error => {
                    console.error(error);
                })
                .finally(() => {
                    this.fetchTableData();
                    this.resetAfter();
                    this.new_button_disabled = true;
                    this.selectedItem = null;
                })
            },
            resetAfter() {
                // Reset after saving
                this.type_select = '';
                this.id_input = '';
                this.count_input = '';
                this.title_input = '';
                this.body_input = '';

                this.can_save = true;
            },
            fetchTableData() {
                // Fetches all rules
                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/all`)
                .then(response => {
                    const rules = response.data.rules.map(rule => ({
                        id: rule.RuleId,
                        count: "Rule #" + rule.count,
                        type: rule.type,
                        title: rule.RuleTitle,
                        body: rule.RuleBody
                    }));

                    // Fetches all guidelines
                    axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/all`)
                    .then(response => {
                        const guidelines = response.data.guidelines.map(guideline => ({
                            id: guideline.GuideId,
                            count: "Guideline #" + guideline.count,
                            type: guideline.type,
                            title: guideline.GuidelineTitle,
                            body: guideline.GuidelineBody
                        }));

                        this.items = [...rules, ...guidelines];

                    })
                    .catch(error => {
                        console.log(error);
                    });
                })
                .catch(error => {
                    console.log(error);
                });
            },
            save() {
                if (this.selectedItem) { // If a row is selected, then update instead
                    return this.update(this.selectedItem);
                }
               
                // Validations
                if (this.type_select.trim().length < 1) {
                    return alert('Please select a type');
                }
                else if (this.title_input.trim().length < 1) {
                    return alert('Please input a title');
                }
                else if (this.title_input.trim().length > 255) {
                    return alert('Title is too long, 255 charactres only');
                }
                else if (this.body_input.trim().length < 1) {
                    return alert('Please input a body');
                }

                // If validation passed, check if can save
                if (this.can_save === false) {
                    return;
                }
                
                // Saving state, set to false for a while to avoid multiple save
                this.can_save = false;

                if (this.type_select === 'rule') {
                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/save`, 
                        { 
                            title: this.title_input, 
                            body: this.body_input 
                        })
                        .then(response => {
                            console.log(response.duration);

                            alert('Rule saved successfully');
                            this.resetAfter();
                        })
                        .catch(error => {
                            console.error(error);
                            this.resetAfter();
                        })
                        .finally(() => {
                            this.fetchTableData(); 
                        });   
                }
                else if (this.type_select === 'guideline') {
                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/save`, 
                        { 
                            title: this.title_input, 
                            body: this.body_input 
                        })
                        .then(response => {
                            console.log(response.duration);

                            alert('Guideline saved successfully');
                            this.resetAfter();
                        })
                        .catch(error => {
                            console.error(error);
                            this.resetAfter();
                        })
                        .finally(() => {
                            this.fetchTableData(); 
                        })
                }
            },
            update(item) {
                // Validations
                if (this.title_input.trim().length < 1) {
                    return alert('Please input a title');
                }
                else if (this.title_input.trim().length > 255) {
                    return alert('Title is too long, 255 characters only');
                }
                else if (this.body_input.trim().length < 1) {
                    return alert('Please input a body');
                }

                // If validation passed, check if can update
                if (this.can_save === false) {
                    return;
                }
                
                // Saving state, set to false for a while to avoid multiple save
                this.can_save = false;

                if (this.type_select === 'rule') {
                    axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/update`, 
                        { 
                            id: this.id_input,
                            title: this.title_input, 
                            body: this.body_input 
                        })
                        .then(response => {
                            console.log(response.duration);

                            alert('Rule updated successfully');
                        })
                        .catch(error => {
                            console.error(error);
                        })
                        .finally(() => {
                            this.can_save = true;
                            this.fetchTableData(); 
                        });   
                }
                else if (this.type_select === 'guideline') {
                    axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/update`, 
                        { 
                            id: this.id_input,
                            title: this.title_input, 
                            body: this.body_input 
                        })
                        .then(response => {
                            console.log(response.duration);

                            alert('Guideline updated successfully');
                        })
                        .catch(error => {
                            console.error(error);
                        })
                        .finally(() => {
                            this.can_save = true;
                            this.fetchTableData(); 
                        })
                }
            },
        },
    }
</script>

<style scoped>
    .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Source Sans', sans-serif;
        margin-right: 3.2%;
    }

    .form-control, .form-select, .body {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .components h2{
        font-weight: 800;
        font-size: 28px;
    }

    .new{
        margin-top: -1%;
        text-align: end;
    }

    .new-btn{
        margin-top: 16px;
        margin-right: 2px;
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 10px 60px 10px 60px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
    }

    .new-btn:disabled{
        background-color: #cccccc;
    }
    
    .save-btn{
        margin-top: 6px;
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 10px 60px 10px 60px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
    }

    .mainbox, .list{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1% 0% -1%;
        padding: 30px 30px 20px 30px;
        border-radius: 7px;
    }

    .body{
        resize: none;
        overflow-y: auto;
        height: 200px;
    }

    .form-group{
        padding-bottom: 15px;
    }

    .save{
        text-align: right;
    }

    .delete-btn{
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 15px 20px 15px 20px;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
    }

    .head{
        text-align: center;
    }

    .form-select:hover{
        cursor: pointer;
    }

    .mainbox, .list {
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    }
    .my-table {
        font-size: 18px;
        font-family: Arial, sans-serif;
        border-collapse: collapse;
    }

    .my-cell {
        border: none;
        text-align: center;
        padding: 10px;
    }

    .my-tbody th,
    .my-tbody td {
        font-weight: normal;
    }

    .my-table tr:hover:not(.active-row) {
        cursor: pointer;
        background-color: #d9ecf3;
    }

    .my-tbody {
        display: block;
        max-height: 180px;
        overflow-y: auto;
    }
    
    .my-thead,
    .my-tbody tr {
        display: table;
        width: 100%;
        table-layout: fixed;
    }

    .my-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .my-table tr:nth-child(odd) {
        background-color: white;
    }

    .my-table thead tr {
        color: #ffffff;
        background-color: #B90321 !important;
    }
    .active-row {
        background-color: #b1dceb !important; /* Change this to your desired color */
    }
</style>