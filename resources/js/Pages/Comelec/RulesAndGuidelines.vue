<template>
    <title>Rules & Guidelines - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row">
            <div class="col-6">
                <h2>RULES & GUIDELINES</h2>
            </div>
            <div class="col-6 new">
                <ActionButton :disabled="new_button_disabled || !can_save" @click="newButtonSelected" class="new-btn">New</ActionButton>
            </div>      
        </div>   
        
        <BaseContainer :height="'auto'" :maxHeight="'600px'">
            <form @submit.prevent="saveOrUpdate">
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
                        <input class="form-control" type="title" name="title" v-model="title_input" :disabled="!can_save">
                    </div>
                    <div class="col-2">
                        <label class="form-label" for="id">ID</label>
                        <input class="form-control" type="id" name="id" v-model="count_input" :disabled="true">
                    </div>
                </div>

                <div>
                    <div class="form-group">
                        <label for="body" class="form-label">Body</label>
                        <textarea class="form-control body" type="text" name="selected-body" v-model="body_input" :disabled="!can_save"></textarea>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <button :disabled="!selectedItem || !can_save" class="delete-btn" @click.prevent="deleteItem">Delete</button>
                    </div>
                    <div class="col-6 save">
                        <ActionButton @submit.prevent="saveOrUpdate" class="save-btn" :disabled="!can_save">{{ saveButtonText }}</ActionButton>
                    </div>
                </div>
            </form>
        </BaseContainer>
        
        <BaseContainer class="item-container" :height="'300px'" :maxHeight="'335px'">
            <BaseTable class="item-table" 
                    :columns="['ID', 'Type', 'Title']" 
                    :tableHeight="'auto'"
                    :maxTableHeight="'235px'">
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
    import { ref, watch, watchEffect } from 'vue';
    import { useQuery, useMutation, useQueryClient  } from "@tanstack/vue-query";

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

            const queryClient = new useQueryClient();

            // Watch type_select(rule/guideline) for changes
            watch(type_select, (newValue) => {
                // Only update count_input.value if no row is selected
                if (!selectedItem.value) {
                    if (newValue === 'rule') {
                        count_input.value = 'Rule #' + (ruleCount.value.count + 1);
                    }
                    else if (newValue === 'guideline') {
                        count_input.value = 'Guideline #' + (guidelineCount.value.count + 1);
                    }
                }
            });

            // Reset after saving or deleting
            const resetAfter = () => {
                type_select.value = '';
                id_input.value = '';
                count_input.value = '';
                title_input.value = '';
                body_input.value = '';

                can_save.value = true;
            };

            // Define the fetch function for rules and guidelines
            const fetchCount = async (endpoint) => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}${endpoint}`);
                return response.data;
            };

            // Use Vue Query to fetch the data
            const { data: ruleCount } = 
                    useQuery({
                        queryKey: ["ruleCount"],
                        queryFn: () => fetchCount('/api/v1/rule/count/latest'),
                    });
            const { data: guidelineCount } = 
                    useQuery({
                        queryKey: ["guidelineCount"],
                        queryFn: () => fetchCount('/api/v1/guideline/count/latest'),
                    });

            // Define the fetch function for rules and guidelines
            const fetchRules = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/all`);

                return response.data.rules.map(rule => ({
                    id: rule.RuleId,
                    count: "Rule #" + rule.count,
                    type: rule.type,
                    title: rule.RuleTitle,
                    body: rule.RuleBody
                }));
            };

            const fetchGuidelines = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/all`);
                
                return response.data.guidelines.map(guideline => ({
                    id: guideline.GuideId,
                    count: "Guideline #" + guideline.count,
                    type: guideline.type,
                    title: guideline.GuidelineTitle,
                    body: guideline.GuidelineBody
                }));
            };

            // Use Vue Query to fetch the data
            const { data: rulesData, isLoading: isRulesDataLoading, dataUpdatedAt: rulesUpdatedAt} = 
                    useQuery({
                        queryKey: ["fetchRules"],
                        queryFn: () => fetchRules(),
                    });

            const { data: guidelinesData, isLoading: isGuidelinesDataLoading } = 
                    useQuery({
                        queryKey: ["fetchGuidelines"],
                        queryFn: () => fetchGuidelines(),
                    });
                    
            // Wait for both rules and guidelines data to load before setting the items
            watchEffect(() => {
                if (!isRulesDataLoading.value && !isGuidelinesDataLoading.value) {
                    items.value = [...rulesData.value, ...guidelinesData.value];
                }
            });

            // Handles saving of an item
            const { mutate: saveMutation, isSuccess: isSaveSucess, isError: isSaveError, isPending: isSavePending } = 
                    useMutation({
                        mutationFn: (item) => axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/${item.type}/save`, item),
                    });

             const saveOrUpdate = () => {
                if (selectedItem.value) { // If a row is selected, then update instead
                    return update();
                }
               
                // Validations
                if (type_select.value.trim().length < 1) {
                    return alert('Please select a type');
                }
                else if (title_input.value.trim().length < 1) {
                    return alert('Please input a title');
                }
                else if (title_input.value.trim().length > 255) {
                    return alert('Title is too long, 255 charactres only');
                }
                else if (body_input.value.trim().length < 1) {
                    return alert('Please input a body');
                }

                // If validation passed, check if can save
                if (can_save.value === false) {
                    return;
                }
                
                // Saving state, set to false for a while to avoid multiple save
                can_save.value = false;

                saveMutation({
                    type: type_select.value,
                    title: title_input.value,
                    body: body_input.value
                }, {
                    onSuccess: async () => {
                        alert('Item saved successfully');
                        resetAfter();

                        queryClient.invalidateQueries('fetchRules');
                        queryClient.invalidateQueries('fetchGuidelines');
                    },
                    onError: (error) => {
                        console.error(error);
                        resetAfter();
                    },
                    onSettled: () => {
                        can_save.value = true;
                    }
                });
            };

            // Handles updating of an item
            const { mutate: updateMutation, isSuccess: isUpdateSucess, isPending: isUpdatePending, isError: isUpdateError } = 
                    useMutation({
                        mutationFn: (item) => axios.put(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/${item.type}/update`, item)
                    });

            const update = () => {
                updateMutation({
                    id: id_input.value,
                    type: type_select.value,
                    title: title_input.value,
                    body: body_input.value
                }, {
                    onSuccess: () => {
                        alert('Item updated successfully');

                        queryClient.invalidateQueries('fetchRules');
                        queryClient.invalidateQueries('fetchGuidelines');
                    },
                    onError: (error) => {
                        console.error(error);
                    },
                    onSettled: () => {
                        can_save.value = true;
                    }
                });
            };

            // Handles deletion of an item
            const { mutate: deleteMutation, isSuccess: isDeleteSuccess, isPending: isDeletePending, isError: isDeleteError } = 
                    useMutation({
                        mutationFn: (id) => axios.delete(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/${type_select.value}/delete`,
                            {
                                data: { id: id }
                            })
                    });

            const deleteItem = () => {
                if (selectedItem.value === null) {
                    return alert('Please select an item to delete');
                }

                const confirmDelete = confirm('Are you sure you want to delete this item?');
                if (!confirmDelete) {
                    return;
                }
                
                deleteMutation(selectedItem.value.id, {
                    onSuccess: () => {
                        alert('Item deleted successfully');
                        resetAfter();
                        new_button_disabled.value = true;
                        selectedItem.value = null;

                        queryClient.invalidateQueries('fetchRules');
                        queryClient.invalidateQueries('fetchGuidelines');
                    },
                    onError: (error) => {
                        console.error(error);
                    }
                });
            };

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
                saveOrUpdate,
                update,
                deleteItem,
                resetAfter
            };
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
        },
    }
</script>

<style scoped>
    .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Inter', sans-serif;
        margin-right: 3.2%;
    }

    .form-control, .form-select, .body {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .components h2{
        font-weight: 800;
        font-size: 30px;
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