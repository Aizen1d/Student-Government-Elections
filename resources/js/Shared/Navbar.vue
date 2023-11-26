<template>
    <nav class="navbar navbar-expand-lg nav navbar-dark">
        <div class="navbar-contents">
            <div>
                <img src="../../images/puplogo.png" alt="" class="puplogo">
                <img src="../../images/pvs.png" alt="" class="pvs-logo">
            </div>
  
            <div class="dropdown">
                <button class="btn btn-link nav-link user" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    {{ full_name }} 
                    <i class="dropdown-toggle"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#" @click="logout">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav> 
</template>

<script>
    import axios from 'axios';
    import { ref } from 'vue';
    import { useUserStore } from '../Stores/UserStore.js';

    export default {
        setup() {

        },
        computed: {
            full_name(){
                return useUserStore().full_name;
            },
        },
        methods: {
            logout(){
                axios.post('/logout')
                    .then(response => {
                        localStorage.setItem('approvalsFilterType', '')
                        useUserStore().reset(); // Reset the user store 
                        location.reload(); // trick the system to logout and prevent backing 
                                         // (Reloading to check for cookie token and throw back to login page)

                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        },
    };
</script>

<style scoped>
   .navbar{
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .navbar-contents{
        margin: 0% 8%;
        display: flex;
        align-items: center;
        width: 100%;
        justify-content: space-between;
    }

    .puplogo{
        width: 58px;
    }

    .pvs-logo{
        width: 170px;
        margin: 0px 30px;
    }

    .logout-button{
        border: transparent;
        background-color: transparent;
        text-align: end;
        font-size: 16px;
    }

    .user,
    .user:hover, 
    .user:active,
    .user:focus
    .user:default{
        color: black;
    }
    .dropdown-toggle{
        margin-left: 7px;
    }

    .dropdown-menu{
        left: inherit;
        right: 0;
        border-radius: 3px;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    }

    .dropdown-item:hover{
        background-color: rgb(207, 207, 207);
    }
</style>