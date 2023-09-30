<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="row utilities">
            <div class="col-5">
                <h2 class="my-1">
                    <span class="return" @click="returnPage">Elections</span> / Create Election
                </h2>
            </div>
        </div>

        <form @submit.prevent="submit">
            <div class="row g-4">
                <div class="col-6">
                    <div class="note">
                        <h6>Set election name and type.</h6>
                    </div>
                    <div class="box upper-box">
                        <label class="form-label" for="name">Election Name</label>
                        <input class="form-control margin" type="text" name="name">
                        
                        <label class="form-label" for="type">Election Type</label>
                        <input type="hidden" name="election-type">
                            <select class="form-select" aria-label="Default select example">
                                <option disabled hidden selected>Select</option>
                                <option value="1">SSC</option>
                                <option value="2">Organization</option>
                            </select>
                    </div>
                </div>
                <div class="col-6">
                    <div class="note">
                        <h6>Set the current school year and semester for this election.</h6>
                    </div>
                    <div class="box upper-box">
                        <label class="form-label" for="sy">School Year</label>
                        <input class="form-control margin" type="text" name="sy">
    
                        <label class="form-label" for="sem">Semester</label>
                        <input class="form-control" type="text" name="sem">
                    </div>
                </div>
            </div>
            
            <div>
                <div class="note-timeline">
                    <h6>Set a timeline for the whole election.</h6>
                </div>
                <div class="box">
                    <div class="row">
                        <label for="election-period" class="col-3 col-form-label">Election Period</label>
                        <div class="col-5">
                            <label class="form-label" for="e-start">Election Start</label>
                            <input type="date" class="form-control margin">

                            <label class="form-label" for="e-end">Election End</label>
                            <input type="date" class="form-control margin">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Filing of COC Period</label>
                        <div class="col-5">
                            <label class="form-label" for="f-start">Filing Start</label>
                            <input type="date" class="form-control margin">

                            <label class="form-label" for="f-end">Filing End</label>
                            <input type="date" class="form-control margin">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Campaign Period</label>
                        <div class="col-5">
                            <label class="form-label" for="c-start">Campaign Start</label>
                            <input type="date" class="form-control margin">

                            <label class="form-label" for="c-end">Campaign End</label>
                            <input type="date" class="form-control margin">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Voting Period</label>
                        <div class="col-5">
                            <label class="form-label" for="v-start">Voting Start</label>
                            <input type="date" class="form-control margin">

                            <label class="form-label" for="v-end">Voting End</label>
                            <input type="date" class="form-control margin">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="row">
                        <label for="filing-period" class="col-3 col-form-label">Appeal Period</label>
                        <div class="col-5">
                            <label class="form-label" for="a-start">Appeal Start</label>
                            <input type="date" class="form-control margin">

                            <label class="form-label" for="a-end">Appeal End</label>
                            <input type="date" class="form-control">
                        </div>
                    </div>
                </div>
            </div>

            <div>
                <div class="note-timeline">
                    <div class="row">
                        <div class="col-6 my-1">
                            <h6>Create positions for the election and set the quantity for each position.</h6>
                        </div>
                        <div class="col-6">
                            <div class="position-btn">
                                <ActionButton class="new-btn" @click="addNewPosition" :disabled="!isMostRecentPositionFilled">Add new position</ActionButton>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="position-box mb-4" v-for="(position, index) in position_list" :key="index">
                    <div class="row g-4">
                        <div class="col">
                            <label class="form-label" for="position-name">Position Name</label>
                            <div class="row">
                                <div class="col-4">
                                    <select class="form-select margin" aria-label="Position selection" v-model="position.value">
                                        <option value="" disabled hidden selected>Saved Positions</option>
                                        <option value="New" style="color: #00ae0c;">Create new</option>
                                        <option v-for="saved_position in position_saved_selection" :value="saved_position.value">
                                            {{ saved_position.name }}
                                        </option>
                                    </select>
                                </div>
                                <div class="col-8">
                                    <input type="text" class="form-control position-name margin" 
                                        v-model="position.name" 
                                        :disabled="position.value !== 'New'">
                                </div>
                            </div>

                            <label class="form-label" for="position-quantity">Position Quantity</label>
                            <input type="number" min="1" class="form-control position-quantity margin" v-model.number="position.quantity">

                            <div class="row button">
                                <div class="col-6">
                                    <button class="remove-btn" 
                                            v-if="index !== 0"
                                            @click="removePosition(index)">Remove position</button>
                                </div>
                                <div class="col-6 save">
                                    <button :disabled="position.name === ''" class="reusable-btn" :style="{ color: position.is_re_usable ? '#00ae0c' : '#B90321' }"
                                            @click.prevent="makePositionReusableOrNot(index)">{{ position.is_re_usable ? 'Make this position reusable' : 'Remove this position re-usability' }}
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="election-btn mb-4">
                    <ActionButton class="cancel">Cancel</ActionButton>
                    <ActionButton class="create">Create Election</ActionButton>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import { useUserStore } from '../../Stores/UserStore';
    import { router } from '@inertiajs/vue3'
    import { ref, watch, computed } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import SearchBarAndFilter from '../../Shared/SearchBarAndFilter.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';

    import axios from 'axios';

    export default{
        setup(props) {
            const userStore = useUserStore();
            const createdByStudentNumber = userStore.student_number;
            
            const position_count = ref(1);
            const position_saved_selection = ref([]);
            const position_list = ref([{
                count: position_count,
                name: '',
                value: '',
                quantity: 1,
                is_re_usable: true,
            }]);

            const watchPosition = (position) => {
                watch(() => position.value, (newVal) => {
                    if (newVal === 'New') {
                        position.name = '';
                    } 
                    else {
                        position.name = newVal;
                    }
                });

                // Determine if the position is reusable or not in initial load
                watch(() => position.name, (newName) => {
                    axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/all`)
                    .then((response) => {
                        const positions = response.data.positions;
                        const positionExists = positions.some((pos) => pos.PositionName === newName);

                        if (positionExists) {
                            position.is_re_usable = false;
                        } 
                        else {
                            position.is_re_usable = true;
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                });
            };

            // Watch for changes in the position list value
            position_list.value.forEach(watchPosition);

            // Get all saved positions in DB and add them to the position saved selection list
            axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/all`)
                .then((response) => {
                    const positions = response.data.positions;
                    
                    positions.forEach((pos) => {
                        const savedPositionsSelection = {
                            name: pos.PositionName,
                            value: pos.PositionName,
                        };
                        position_saved_selection.value.push(savedPositionsSelection);
                    });
                })
                .catch((error) => {
                    console.log(error);
                });

            // Return true if the most recent position is filled, if true enable the add new position button
            const isMostRecentPositionFilled = computed(() => {
                const mostRecentPosition = position_list.value[position_list.value.length - 1];
                return mostRecentPosition.name !== '' && mostRecentPosition.quantity > 0;
            });

            return { createdByStudentNumber, position_count, position_list, isMostRecentPositionFilled, position_saved_selection}
        },
        components: { Navbar, Sidebar, ActionButton, SearchBarAndFilter, BaseContainer, BaseTable, },
        props: {
            full_name: String,
            user_role: String,
        },
        methods:{
            returnPage(){
                router.visit('/comelec/elections');
            },
            addNewPosition() {
                this.position_count = this.position_count + 1;
                const newPosition = {
                    count: this.position_count,
                    name: '',
                    value: '',
                    quantity: 1,
                };
                this.position_list.push(newPosition);
                this.watchPositionValue();
            },
            removePosition(index) {
                this.position_list.splice(index, 1);
            },
            watchPositionValue() {
                this.position_list.forEach((position, index) => {
                    watch(() => position.value, (newVal) => {
                        if (newVal === 'New') {
                            position.name = '';
                        } 
                        else {
                            position.name = newVal;
                        }
                    });
                });

                this.position_list.forEach((position, index) => {
                    watch(() => position.name, (newName) => {
                        axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/all`)
                        .then((response) => {
                            const positions = response.data.positions;
                            const positionExists = positions.some((pos) => pos.PositionName === newName);

                            if (positionExists) {
                                position.is_re_usable = false;
                            } 
                            else {
                                position.is_re_usable = true;
                            }
                        })
                        .catch((error) => {
                            console.log(error);
                        });
                    });
                });
            },
            refreshPositionListAndReusabilityState() {
                this.position_list.forEach((position, index) => {
                    axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/all`)
                    .then((response) => {
                        const positions = response.data.positions;
                        const positionExists = positions.some((pos) => pos.PositionName === position.name);

                        if (positionExists) {
                            position.is_re_usable = false;
                        } 
                        else {
                            position.value = '';
                            position.name = '';
                            position.is_re_usable = true;
                        }

                        this.position_saved_selection = [];
                        positions.forEach((pos) => {
                            const savedPositionsSelection = {
                                name: pos.PositionName,
                                value: pos.PositionName,
                            };
                            this.position_saved_selection.push(savedPositionsSelection);
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                });
            },
            makePositionReusableOrNot(index){    
                const position = this.position_list[index]
                const name = position.name.trim();

                if (position.is_re_usable) {
                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/reusable/save`, {
                        name: name
                    }) 
                    .then((response) => {
                        this.refreshPositionListAndReusabilityState();
                        position.value = name.charAt(0).toUpperCase() + name.slice(1);

                        alert(response.data.message)
                        console.log(response.duration);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                }
                else {
                    axios.delete(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/position/reusable/delete`, {
                        data: {
                            name: name
                        }
                    })
                    .then((response) => {
                        this.refreshPositionListAndReusabilityState();

                        alert(response.data.message)
                        console.log(response.duration);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                }
            },
            submit(){
                for (const value of this.position_list) {
                    console.log(value.name);
                }
            }
        }
    }
</script>

<style scoped>
    .utilities{
        margin-bottom: 1%;
    }

    .return{
        color: #B90321;
        cursor: pointer;
    }

    .return:hover{
        text-decoration: underline;
    }

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
    
    .form-control, .form-select {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .margin{
        margin-right: -1%;
        margin-left: -1%;
    }

    .button{
        margin-top: 5%;
    }

    .save{
        text-align: end;
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

    .note-timeline{
        margin-top: 1.5%;
        background-color: #FDD5D5;
        padding: 1.1%;
    }

    .note-timeline h6{
        margin-top: 10px;
    }

    .box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 3%;
    }

    .upper-box{
        padding-bottom: 5%;
    }

    .position-box{
        background-color: white;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.14), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
        padding: 3% 3% 2% 3%;
    }

    .margin{
        margin-bottom: 2%;
        margin-left: 0%;
    }

    .list{
        margin-top: 3.5%;
    }

    .head{
        text-align: center;
    }

    .position-btn{
        text-align: end;
    }

    .election-btn{
        text-align: end;
    }

    .new-btn{
        margin-top: .5%;
    }

    .remove-btn {
        margin-left: -1%;
        margin-top: -10%;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
    }

    .remove-btn:hover{
        color: #B90321;
    }

    .remove-btn:disabled{
        color: #cccccc;
    }

    .reusable-btn {
        margin-top: -10% !important;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #00ae0c;
    }

    .reusable-btn:hover{
        color: rgb(12, 194, 2);
    }

    .reusable-btn:disabled{
        color: #cccccc !important;
    }

    .cancel{
        color: black;
        background-color: #FDD5D5;
        margin-right: 2%;
    }

    .cancel:hover{
        background-color: #ffcfcf;
    }
</style>