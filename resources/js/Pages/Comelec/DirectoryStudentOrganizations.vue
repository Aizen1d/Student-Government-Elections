<template>
    <title>Directory Election Winners - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h2 class="my-1 page-title">
                <span class="return" @click="returnDirectory">Directory</span> > <span class="return" @click="returnDirectory">Student Organizations</span> > Create Organization
            </h2>
        </div>

        <div class="row g-4">
            <div class="col-6">
                <div class="note">
                    <span>Set the organization name, logo, and member requirements.</span>
                </div>
                <div class="content row" style="height: 33.5% !important;">
                    <div class="col-3 upload">
                        <img src="../../../images/icons/default-org.png" alt="" class="organization-logo">
                        <div class="round">
                            <input type="file">
                            <i class = "fa fa-camera" style = "color: #fff;"></i>
                            </div>
                    </div>
                    <div class="col info">
                        <label class="form-label" for="name">Organization Name</label>
                        <input class="form-control margin" type="text" name="name">
                        
                        <label class="form-label" for="selected">Member Requirements</label>
                        <input type="hidden" name="requirements">
                        <select class="form-select padding" aria-label="Default select example">
                            <option selected>Select</option>
                            <option value="1">All</option>
                            <option value="2">BBTLEDHE</option>
                            <option value="3">BSBAHRM</option>
                            <option value="4">BSBA-MM</option>
                            <option value="5">BSENTREP</option>
                            <option value="6">BSIT</option>
                            <option value="7">BPAPFM</option>
                            <option value="8">DOMTMOM</option>
                        </select>
                    </div>
                </div>   
                
                <div class="note mt-4">
                    <span>Set the organization adviser, vision, and mission.</span>
                </div>
                <div class="content row">
                    <div class="col info">
                        <label class="form-label" for="adviser">Adviser Name</label>
                        <input class="form-control margin1" type="text" name="adviser">
                        
                        <label class="form-label" for="vision">Vision</label>
                        <input class="form-control margin1" type="text" name="vision">
                        
                        <label class="form-label" for="mission">Mission</label>
                        <input class="form-control padding1" type="text" name="mission">
                    </div>
                </div>     
            </div>

            <div class="col-6">
                <div class="note">
                    <span>Set the organization officers.</span>
                </div>
                
                <div class="content row">
                    <div class="header">
                        <span class="header-label">Organization Officers</span>
                        <button class="add-button"><img src="../../../images/icons/add.svg" alt="" class="add-svg"></button>
                    </div>
                    <div class="col info">
                        <label class="form-label" for="position">Position</label>
                        <input class="form-control margin" type="text" name="position">
                        
                        <label class="form-label" for="officer">Officer Name</label>
                        <input class="form-control" type="text" name="officer">
                    </div>
                    <div class="col-3 upload1">
                        <img src="../../../images/icons/default-org.png" alt="" class="organization-logo">
                        <div class="round1">
                            <input type="file">
                            <i class = "fa fa-camera" style = "color: #fff;"></i>
                        </div>
                    </div>
                </div>   
                
                <div class="note" style="margin-top: 3%;">
                    <span>Set the organization members.</span>
                </div>
                <div class="content row">
                    <div class="header">
                        <span class="header-label">Organization Members</span>
                        <button class="add-button"><img src="../../../images/icons/add.svg" alt="" class="add-svg"></button>
                    </div>
                    <div class="col info">
                        <label class="form-label" for="member">Member Name</label>
                        <input class="form-control margin1" type="text" name="member">

                        <div class="group">
                            <label class="form-label" for="member">Member Name</label>
                            <button class="delete-button"><img src="../../../images/icons/delete.svg" alt="" class="delete-svg"></button>
                        </div>  
                        <input class="form-control margin1" type="text" name="member">

                        <!--IMPORTANT NOTE!!! KAPAG LAST MEMBER DAPAT MAY PADDING1 SA CLASS NIYA-->
                        <div class="group">
                            <label class="form-label" for="member">Member Name</label>
                            <button class="delete-button"><img src="../../../images/icons/delete.svg" alt="" class="delete-svg"></button>
                        </div>  
                        <input class="form-control padding1" type="text" name="member">
                    </div>   
                </div>
            </div>
        </div>

        <div class="box">
            <div class="buttons">
                <button class="cancel-button">Cancel</button>
                <button class="create-button">Create</button>
            </div>
        </div>
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
        methods: {
            returnDirectory() {
                router.visit('/comelec/directory');
            }
        }
    }
</script>

<style scoped>
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

    .return{
        color: #B90321;
        cursor: pointer;
    }

    .return:hover{
        text-decoration: underline;
    }

    .page-title{
        font-weight: 900;
        font-size: 28px;
        margin: 0%;
    }

    .main{
        margin: -1%;
        margin-top: -2%;
        font-family: 'Inter', sans-serif;
    } 

    .note{
        background-color: #F2F2F2;
        padding: 2%;
        font-size: 16px;
    }

    .content{
        background-color: white;
        padding: 3%;
        display: flex;
        align-items: center;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        margin: 0%;
    }

    .organization-logo{
        width: 100%;
        height: 100%;
    }

    .margin{
        margin-bottom: 4%;
    }

    .margin1{
        margin-bottom: 3%;
    }

    .padding{
        margin-bottom: 1%;
    }

    .padding1{
        margin-bottom: 0.8%;
    }

    .header{
        justify-content: left;
        margin-bottom: 3%;
    }

    .header-label{
        margin: 0% 0.9%;
        font-weight: 600;
        font-size: 16px;
    }

    .add-button, .delete-button{
        border: transparent;
        background-color: transparent;
        margin: 0%;
        padding: 0%;
    }

    .add-svg{
        width: 30px;
    }

    .delete-svg{
        width: 30px;
        margin-bottom: 7px;
    }

    .delete-button:hover{
        .delete-svg{
            filter: invert(16%) sepia(96%) saturate(2668%) hue-rotate(357deg) brightness(97%) contrast(92%);
        }
    }

    .group{
        display: flex;
        justify-content: space-between;
    }

    .box{
        margin: 1.5% 0%;
    }

    .buttons{
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        background-color: white;
        border-radius: 7px;
        padding: 20px;
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


    .upload{
        width: 135px;
        position: relative;
        margin-right: 4%;
        padding: 0%;
    }
    
    .upload img{
        border-radius: 50%;
        border: 6px solid #eaeaea;
    }
    
    .upload .round{
        position: absolute;
        bottom: 0;
        right: 0;
        background: #D9D9D9;
        width: 32px;
        height: 32px;
        line-height: 33px;
        text-align: center;
        border-radius: 50%;
        overflow: hidden;
    }
    
    .upload .round input[type = "file"]{
        position: absolute;
        transform: scale(2);
        opacity: 0;
    }

    .upload1{
        width: 135px;
        position: relative;
        margin-left: 4%;
        padding: 0%;
    }
    
    .upload1 img{
        border-radius: 50%;
        border: 6px solid #eaeaea;
    }
    
    .upload1 .round1{
        position: absolute;
        bottom: 0;
        right: 0;
        background: #D9D9D9;
        width: 32px;
        height: 32px;
        line-height: 33px;
        text-align: center;
        border-radius: 50%;
        overflow: hidden;
    }
    
    .upload1 .round1 input[type = "file"]{
        position: absolute;
        transform: scale(2);
        opacity: 0;
    }
    
    input[type=file]::-webkit-file-upload-button{
        cursor: pointer;
    }

    .round:hover, .round1:hover{
        background-color: #c3c1c1;
    }
</style>