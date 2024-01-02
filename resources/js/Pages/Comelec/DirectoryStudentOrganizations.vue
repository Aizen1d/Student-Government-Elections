<template>
    <title>Directory Student Organizations - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <div class="components">
        <div class="header">
            <h2 class="my-1 page-title">
                <span class="return" @click="returnDirectory">Directory</span> > <span class="return" @click="returnDirectory">Student Organizations</span> > Create Organization
            </h2>
        </div>

        <div class="row">
            <div class="col-6" style="height: 100%;">
                <div class="note">
                    <span>Set the organization name, logo, and member requirements.</span>
                </div>
                <div class="content row" style="height: 255px">
                    <div class="col-3 upload">
                        <img v-if="organization_logo === ''" src="../../../images/icons/default-org.png" alt="" class="organization-logo">
                        <img v-else :src="organization_logo" alt="" class="organization-logo">
                        <div class="round">
                            <input :disabled="creating" type="file" accept="image/*" @change="previewImageLogo($event)">
                            <i class = "fa fa-camera" style = "color: black;"></i>
                        </div>
                    </div>
                    <div class="col info">
                        <label class="form-label" for="name">Organization Name</label>
                        <input :disabled="creating" class="form-control margin" type="text" name="name" v-model="organization_name">
                        
                        <label class="form-label" for="selected">Member Course Requirements</label>
                        <input :disabled="creating" type="hidden" name="requirements">
                        <select class="form-select padding" aria-label="Default select example" v-model="organization_requirements">
                            <option selected hidden value="">Select</option>
                            <option value="All">All</option>
                            <option value="BBTLEDHE">BBTLEDHE</option>
                            <option value="BSBAHRM">BSBAHRM</option>
                            <option value="BSBA-MM">BSBA-MM</option>
                            <option value="BSENTREP">BSENTREP</option>
                            <option value="BSIT">BSIT</option>
                            <option value="BPAPFM">BPAPFM</option>
                            <option value="DOMTMOM">DOMTMOM</option>
                        </select>
                    </div>
                </div>   
                
                <div class="note mt-4">
                    <span>Set the organization adviser, image, vision, and mission.</span>
                </div>
                <div class="content row">
                    <div class="col-3 upload">
                        <img v-if="organization_adviser_image === ''" src="../../../images/icons/default-org.png" alt="" class="organization-logo">
                        <img v-else :src="organization_adviser_image" alt="" class="organization-logo">
                        <div class="round">
                            <input :disabled="creating" type="file" accept="image/*" @change="previewImageAdviserImage($event)">
                            <i class = "fa fa-camera" style = "color: black;"></i>
                        </div>
                    </div>
                    <div class="col info">
                        <label class="form-label" for="adviser">Adviser Name</label>
                        <input :disabled="creating" class="form-control margin1" type="text" name="adviser" v-model="organization_adviser_name">
                        
                        <label class="form-label" for="vision">Vision <span style="font-family: Arial; font-size: 14px;">(Optional)</span></label>
                        <input :disabled="creating" class="form-control margin1" type="text" name="vision" v-model="organization_vision">
                        
                        <label class="form-label" for="mission">Mission <span style="font-family: Arial; font-size: 14px;">(Optional)</span></label>
                        <input :disabled="creating" class="form-control padding1" type="text" name="mission" v-model="organization_mission">
                    </div>
                </div>     
            </div>

            <div class="col-6">
                <div class="note">
                    <span>Set the organization officers.</span>
                </div>
                
                <div class="content row flex-column">
                    <div class="header">
                        <span class="header-label">Organization Officers ({{ officers_count + 1 }})</span>
                        <button @click="addOfficer" class="add-button" :disabled="creating"><img src="../../../images/icons/add.svg" draggable="false" class="add-svg"></button>
                    </div>
                    <template v-for="(officer, officer_index) in officers" :key="officer_index">
                        <hr v-if="officer_index !== 0" style="margin-top: 5%; margin-bottom: 5%;"/> <!-- Add hr on newly added not in the first index -->
                        <div class="d-flex flex-row align-items-start">
                            <div class="col info">
                                <div class="row">
                                    <div class="col-6">
                                        <label class="form-label" for="officer">Student Number
                                            <i class="fa fa-spinner fa-spin fa-1x" v-if="officer.checking"></i>
                                        </label>
                                        <input :disabled="creating" class="form-control margin" type="text" name="officer" v-model="officer.student_number" @keyup="debouncedGetOfficerFullName(officer)">
                                    </div>
                                    <div class="col-6">
                                        <label class="form-label" for="officer">Officer Name</label>
                                        <input class="form-control margin" :style="{ color: !officer.existing ? '#B90321' : 'black'}" type="text" name="officer" v-model="officer.name" disabled>
                                    </div>
                                </div>

                                <label class="form-label" for="position">Position</label>
                                <input :disabled="creating" class="form-control" type="text" name="position" v-model="officer.position">
                            </div>  
                            <div class="col-3 upload1">
                                <img v-if="officer.image === ''" src="../../../images/icons/default-org.png" class="organization-logo">
                                <img v-else :src="officer.image" alt="" class="organization-logo">
                                <div class="round1">
                                    <input :disabled="creating" type="file" accept="image/*" @change="previewImageOfficer($event, officer)">
                                    <i class = "fa fa-camera" style = "color: black;"></i>
                                </div>
                            </div>
                            <button v-if="officer_index !== 0" class="delete-button" @click="removeOfficer(officer_index)" :disabled="creating"><img src="../../../images/icons/delete.svg" draggable="false" class="delete-svg"></button> <!-- Add delete button -->
                        </div>
                    </template>
                </div>
                
                <div class="note" style="margin-top: 3%;">
                    <span>Set the organization members.</span>
                </div>
                <div class="content row flex-column">
                    <div class="header">
                        <span class="header-label">Organization Members ({{ members_count + 1 }})</span>
                        <button @click="addMember" class="add-button" :disabled="creating"><img src="../../../images/icons/add.svg" class="add-svg" draggable="false"></button>
                    </div>
                    <template v-for="(member, member_index) in members" :key="member_index">
                        <div class="col info">
                            <template v-if="member_index === 0">
                                <div class="row">
                                    <div class="col-6">
                                        <label class="form-label" for="member">Student Number
                                            <i class="fa fa-spinner fa-spin fa-1x" v-if="member.checking"></i>
                                        </label>
                                        <input :disabled="creating" class="form-control margin" type="text" name="member" v-model="member.student_number" @keyup="debouncedGetMemberFullName(member)">
                                    </div>
                                    <div class="col-6">
                                        <label class="form-label" for="member">Member Name</label>
                                        <input class="form-control margin1" :style="{ color: !member.existing ? '#B90321' : 'black'}" type="text" name="member" v-model="member.name" disabled>
                                    </div>
                                </div>
                            </template>
                            <template v-else>
                                <div class="row">
                                    <hr style="margin-bottom: 3%;">
                                    <div class="col-6">
                                        <label class="form-label" for="member">Student Number
                                            <i class="fa fa-spinner fa-spin fa-1x" v-if="member.checking"></i>
                                        </label>
                                        <input :disabled="creating" class="form-control margin" type="text" name="member" v-model="member.student_number" @keyup="debouncedGetMemberFullName(member)">
                                    </div>
                                    <div class="col-6">
                                        <div class="group">
                                            <label class="form-label" for="member">Member Name</label>
                                            <button @click="removeMember(member_index)" class="delete-button" :disabled="creating"><img src="../../../images/icons/delete.svg" alt="" class="delete-svg" draggable="false"></button>
                                        </div>  
                                        <input class="form-control margin1" :style="{ color: !member.existing ? '#B90321' : 'black'}" type="text" name="member" v-model="member.name" disabled>
                                    </div>                                    
                                </div>
                            </template>
                        </div>   
                    </template>
                </div>
                
            </div>
        </div>

        <div class="box">
            <div class="buttons">
                <button @click="returnDirectory" :disabled="creating" class="cancel-button">Cancel</button>
                <ActionButton @click="create" :disabled="creating" class="create-button">Create</ActionButton>
            </div>
        </div>
    </div>
</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watch, watchEffect, reactive } from 'vue';

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
            const organization_name = ref('');
            const organization_requirements = ref('');
            const organization_logo = ref('');

            const organization_adviser_name = ref('');
            const organization_adviser_image = ref('');
            const organization_vision = ref('');
            const organization_mission = ref('');

            const creating = ref(false);

            const officers_count = ref(0);
            const officers = reactive([
                                    { 
                                        student_number: '',
                                        checking: false,
                                        existing: false,
                                        name: '',
                                        position: '',
                                        image: ''
                                    }
            ]);

            const members_count = ref(0);
            const members = ref([
                                    { 
                                        student_number: '',
                                        checking: false,
                                        existing: false,
                                        name: '',
                                    }
            ]);

            const getOfficerFullName = async (officer) => {
                if (officer.student_number && officer.student_number !== '') {

                    let studentNumberExistsInOtherOrganization = false;

                    // Check if student number exists in other organization
                    await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/organization/officer/existing/${officer.student_number}`)
                    .then(response => {
                        studentNumberExistsInOtherOrganization= response.data.response;
                    })
                    .catch(error => {
                        console.log(error);
                    })

                    // If student number exists in other organization, return
                    if (studentNumberExistsInOtherOrganization) {
                        officer.checking = false;
                        officer.name = 'Exists in other organization.';
                        officer.existing = false;
                        return;
                    }

                    axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/fullname/${officer.student_number}`)
                    .then(response => {
                        officer.name = response.data.full_name;
                        officer.existing = true;
                    })
                    .catch(error => {
                        officer.name = 'Student does not exist.';
                        officer.existing = false;
                    })
                    .finally(() => {
                        officer.checking = false;
                    })
                }
                else {
                    officer.checking = false;
                    officer.name = '';
                    officer.existing = false;
                }
            }

            let officerTimeoutId;

            const debouncedGetOfficerFullName = (officer) => {
                if (officer.student_number === '') {
                    officer.checking = false;
                    officer.name = '';
                    officer.existing = false;

                    return;
                }
                officer.checking = true;
                officer.existing = false;

                clearTimeout(officerTimeoutId);
                officerTimeoutId = setTimeout(() => getOfficerFullName(officer), 500);
            }

            // Member stuffs

            const getMemberFullName = async (member) => {
                if (member.student_number && member.student_number !== '') {

                    let studentNumberExistsInOtherOrganization = false;

                    // Check if student number exists in other organization
                    await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/organization/member/existing/${member.student_number}`)
                    .then(response => {
                        studentNumberExistsInOtherOrganization= response.data.response;
                    })

                    // If student number exists in other organization, return
                    if (studentNumberExistsInOtherOrganization) {
                        member.checking = false;
                        member.name = 'Exists in other organization.';
                        member.existing = false;
                        return;
                    }

                    axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/fullname/${member.student_number}`)
                    .then(response => {
                        member.name = response.data.full_name;
                        member.existing = true;
                    })
                    .catch(error => {
                        member.name = 'Student does not exist.';
                        member.existing = false;
                    })
                    .finally(() => {
                        member.checking = false;
                    })
                }
                else {
                    member.checking = false;
                    member.name = '';
                    member.existing = false;
                }
            }
            
            let memberTimeoutId;

            const debouncedGetMemberFullName = (member) => {
                if (member.student_number === '') {
                    member.checking = false;
                    member.name = '';
                    member.existing = false;

                    return;
                }
                member.checking = true;
                member.existing = false;

                clearTimeout(memberTimeoutId);
                memberTimeoutId = setTimeout(() => getMemberFullName(member), 500);
            }

            return {
                organization_name,
                organization_requirements,
                organization_logo,

                organization_adviser_name,
                organization_adviser_image,
                organization_vision,
                organization_mission,

                creating,

                officers_count,
                officers,

                members_count,
                members,

                getOfficerFullName,
                debouncedGetOfficerFullName,

                getMemberFullName,
                debouncedGetMemberFullName,
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
            },
            addOfficer() {
                this.officers_count++;
                this.officers.push({ 
                                        student_number: '',
                                        checking: false,
                                        existing: false,
                                        name: '',
                                        position: '',
                                        image: ''
                });
            },
            removeOfficer(index) {
                // Remove officer from array base on index
                this.officers.splice(index, 1);
                this.officers_count--;
            },
            addMember() {
                this.members_count++;
                this.members.push({ 
                                    student_number: '',
                                    checking: false,
                                    existing: false,
                                    name: '',
                });
            },
            removeMember(index) {
                // Remove member from array base on index
                this.members.splice(index, 1);
                this.members_count--;
            },
            previewImageOfficer(event, officer) {
                const reader = new FileReader();
                reader.onload = e => {
                    officer.image = e.target.result;
                };
                reader.readAsDataURL(event.target.files[0]);
            },
            previewImageLogo(event) {
                const reader = new FileReader();
                reader.onload = e => {
                    this.organization_logo = e.target.result;
                };
                reader.readAsDataURL(event.target.files[0]);
            },
            previewImageAdviserImage(event) {
                const reader = new FileReader();
                reader.onload = e => {
                    this.organization_adviser_image = e.target.result;
                };
                reader.readAsDataURL(event.target.files[0]);
            },
            validate() {
                // Validate one by one
                if (this.organization_logo === '') {
                    alert('Please input organization logo.');
                    return false;
                }
                if (this.organization_name === '') {
                    alert('Please input organization name.');
                    return false;
                }
                if (this.organization_requirements === '') {
                    alert('Please input organization requirements.');
                    return false;
                }

                if (this.organization_adviser_image === '') {
                    alert("Please input adviser's image.");
                    return false;
                }
                if (this.organization_adviser_name === '') {
                    alert('Please input adviser name.');
                    return false;
                }

                // validate each officer
                for(let i = 0; i <= this.officers_count; i++) {
                    if (this.officers[i].student_number === '') {
                        alert(`Please input officer student number at row ${i + 1}.`);
                        return false;
                    }

                    if (this.officers[i].existing === false) {
                        alert(`Please resolve problem at row ${i + 1}.`)
                        return false;
                    }

                    // Check for duplicate student numbers
                    for(let j = 0; j < i; j++) {
                        if (this.officers[j].student_number === this.officers[i].student_number) {
                            alert(`Duplicate officer student number found at rows ${j + 1} and ${i + 1}.`);
                            return false;
                        }
                    }

                    if (this.officers[i].position === '') {
                        alert(`Please input officer position at row ${i + 1}.`);
                        return false;
                    }

                    if ( this.officers[i].image === '') {
                        alert(`Please input officer image at row ${i + 1}.`);
                        return false;
                    }

                }

                // validate each member
                for(let i = 0; i <= this.members_count; i++) {
                    if (this.members[i].student_number === '') {
                        alert(`Please input member student number at row ${i + 1}.`);
                        return false;
                    }
                    
                    if (this.members[i].existing === false) {
                        alert(`Please resolve problem at row ${i + 1}.`)
                        return false;
                    }

                    for(let j = 0; j < i; j++) {
                        if (this.members[j].student_number === this.members[i].student_number) {
                            alert(`Duplicate member student number found at rows ${j + 1} and ${i + 1}.`);
                            return false;
                        }
                    }
                }

                return true;
            },
            create(){
                if (this.validate()) {

                    const data = {
                        organization_logo: this.organization_logo,
                        organization_name: this.organization_name,
                        organization_requirements: this.organization_requirements,
                        organization_adviser_image: this.organization_adviser_image,
                        organization_adviser_name: this.organization_adviser_name,
                        organization_vision: this.organization_vision,
                        organization_mission: this.organization_mission,
                        officers: this.officers,
                        members: this.members,
                    };

                    this.creating = true;

                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/organization/create`, data)
                    .then(response => {
                        alert(response.data.message);
                        this.returnDirectory();
                    })
                    .catch(error => {
                        console.log(error);
                        alert(error.data)
                    })
                    .finally(() => {
                        this.creating = false;
                    })                    
                }
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
        width: 145px;
        height: 145px;
        object-fit: cover;
        border-radius: 100px;
        outline: 1px solid #bbbb;
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