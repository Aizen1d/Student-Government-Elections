<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>Rules & Guidelines</h2>
            </div>
            <div class="col-6 new">
                <ActionButton :disabled="new_button_disabled" @click="newButtonSelected" class="new-btn">New</ActionButton>
            </div>      
        </div>   
        
        <BaseContainer :height="'auto'">
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
                        <button :disabled="!selectedItem" class="delete-btn" @click.prevent="deleteItem">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <ActionButton @submit.prevent="save" class="save-btn">{{ saveButtonText }}</ActionButton>
                    </div>
                </div>
            </form>
        </BaseContainer>
        
        <BaseContainer class="item-container" :height="'300px'">
            <BaseTable class="item-table" :columns="['ID', 'Type', 'Title']" :table-height="'200px'">
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
    import { Link } from '@inertiajs/vue3'
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import ActionButton from '../../Shared/ActionButton.vue';

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
                        const data = response.data;

                        if (data.count === 0) {
                            count_input.value = prefix + 1;
                        }
                        else {
                            count_input.value = prefix + (data.count + 1);
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
                        updateIdInput('Rule #', '/api/v1/rule/count/latest')();
                    }
                    else if (newValue === 'guideline') {
                        updateIdInput('Guideline #', '/api/v1/guideline/count/latest')();
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
        components: { Link, Navbar, Sidebar, BaseTable, BaseContainer, ActionButton },
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

                const confirmDelete = confirm('Are you sure you want to delete this item?');
                if (!confirmDelete) {
                    return;
                }
                
                let id = this.selectedItem.id;
                let type = this.selectedItem.type;

                axios.delete(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/${type}/delete`, {
                    data: { id: id }
                })
                .then(response => {
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
                    return this.update();
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
            update() {
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

    .item-container{
        margin-bottom: 2%;
    }

    .new{
        margin-top: -1%;
        text-align: end;
    }

    .new-btn{
        margin-top: 1%;
    }

    .new-btn:disabled{
        background-color: #cccccc;
    }

    .list{
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

    .save-btn{
        margin-top: 1%;
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

    .delete-btn:hover{
        color: #B90321;
    }

    .delete-btn:disabled{
        color: #bbbbbb;
    }

    .head{
        text-align: center;
    }

    .form-select:hover{
        cursor: pointer;
    }

    .list {
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    }
</style>