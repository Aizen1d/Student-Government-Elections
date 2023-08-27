<template>
    <nav class="navbar navbar-expand-lg nav navbar-dark">
        <div class="container-fluid">
            <div class="collapse navbar-collapse">
            </div>
            <li class="nav-item dropdown">
                <button class="btn btn-link nav-link dropdown-toggle mx-4 user" href="#" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    User
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#" @click="logout">Logout</a></li>
                </ul>
            </li>
        </div>
    </nav>  
</template>

<script>
    import axios from 'axios';
    import { Link } from '@inertiajs/vue3'

    export default {
        methods: {
            logout(){
                axios.post('/logout')
                    .then(response => {
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
@import url(../../css/standard.css);
    .nav{
        background-color: white;
        box-shadow: rgba(0, 0, 0, 0.15) 4.8px 1px 3px;
        z-index: 1;
    }

    .system{
        color: #800000;
        font-size: 20px;
    }

    .content{
        color: black;
        font-size: 17px;
        transition: all 0.15s ease-out;
    }

    .content:active,
    .content:hover,
    .content:focus{
        color: black;
        transform: scale(1.05);
    }

    .user{
        color: black;
    }

    .user:hover, 
    .user:active,
    .user:focus
    .user:default{
        color: black;
    }

    .navbar-active{
        color: black;
    }

    .dropdown-item:hover{
        color: white;
        background-color: var(--light_blue);
    }

    .logout{
        justify-content: right;
    }
</style>