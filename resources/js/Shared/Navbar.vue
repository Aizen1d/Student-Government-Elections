<template>
    <nav class="navbar navbar-expand-lg nav navbar-dark">
        <div class="container-fluid">
            <div class="collapse navbar-collapse">
            </div>
            <li class="nav-item dropdown">
                <button class="btn btn-link nav-link dropdown-toggle mx-4 user" href="#" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    John Doe
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="{{ route('faculty-profile') }}">Profile</a></li>
                    <li><a class="dropdown-item" href="{{ route('logout-faculty') }}">Logout</a></li>
                </ul>
            </li>
        </div>
    </nav>  
</template>

<script>
    import { Link } from '@inertiajs/vue3'

    export default {
        components: { Link }, 
    };
</script>

<style>
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