<template>
    <title>Directory - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h1 class="page-title">Create Certification</h1>
        </div>

        <form action="">
            <div class="mainbox">
                <div class="form-group">
                    <label class="form-label" for="title">Title</label>
                    <input class="form-control" type="text" name="title">
                </div>
                <div class="form-group">
                    <label class="form-label" for="date">Date</label>
                    <input class="form-control" type="date" name="date">
                </div>
                <div class="form-group">
                    <label class="form-label" for="name">Name</label>
                    <input class="form-control" type="text" name="name">
                </div>
                <div class="form-group">
                    <label class="form-label" for="position">Position</label>
                    <input class="form-control" type="text" name="position">
                </div>
            </div>

            <div class="signatories">                    
                <div class="form-group">
                    <label class="form-label" for="selected">Signatory</label>
                    <input type="hidden" name="signatory">
                    <select class="form-select" aria-label="Default select example">
                        <option selected>Select</option>
                        <option value="1">Roselyn Viray</option>
                        <option value="2">Leandro Avena</option>
                        <option value="3">David Daniel Reataza</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="signatory-title">Signatory Position</label>
                    <input class="form-control" type="text" name="signatory-title">
                </div>
            </div>

            <div class="signatories">                    
                <div class="form-group">
                    <label class="form-label" for="selected">Signatory</label>
                    <input type="hidden" name="signatory">
                    <select class="form-select" aria-label="Default select example">
                        <option selected>Select</option>
                        <option value="1">Roselyn Viray</option>
                        <option value="2">Leandro Avena</option>
                        <option value="3">David Daniel Reataza</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="signatory-title">Signatory Position</label>
                    <input class="form-control" type="text" name="signatory-title">
                </div>
            </div>

            <div class="signatories">                    
                <div class="form-group">
                    <label class="form-label" for="selected">Signatory</label>
                    <input type="hidden" name="signatory">
                    <select class="form-select" aria-label="Default select example">
                        <option selected>Select</option>
                        <option value="1">Roselyn Viray</option>
                        <option value="2">Leandro Avena</option>
                        <option value="3">David Daniel Reataza</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="signatory-title">Signatory Position</label>
                    <input class="form-control" type="text" name="signatory-title">
                </div>
            </div>

            <div class="buttons">
                <button class="cancel-button">Cancel</button>
                <button class="create-button">Create</button>
            </div>
        </form>      
    </div>

</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watch, watchEffect } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import ImageSkeleton from '../../Skeletons/ImageSkeleton.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';

    export default {
        setup() {

            return {

            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            BaseContainer,
            BaseTable,
            ImageSkeleton,
        },
    }
</script>

<style scoped>
    /*!!!START OF CSS!!!*/

    .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Inter', sans-serif;
        margin-right: 3%;
    }

    .header{
        display: flex;
        align-items: center;
        margin: 0% -1%;
        justify-content: space-between;
    }

    .page-title{
        font-weight: 900;
        font-size: 28px;
        margin: 0%;
    }

    .mainbox, .list, .signatories, .buttons{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1%;
        padding: 30px 30px 20px 30px;
        border-radius: 7px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        width: 50%;
    }

    .body{
        height: 200px;
    }

    .form-group{
        padding-bottom: 15px;
    }

    .buttons{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .cancel-button{
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 15px 20px 15px 20px;
        border: transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CC3300;
    }

    .create-button{
        padding: 13px 50px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
    }
</style>