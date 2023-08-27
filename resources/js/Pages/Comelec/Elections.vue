<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="container">
        <h1>Elections</h1>
        <p>Student Number: {{ student_number }}</p>
        <p>Position: {{ position }}</p>
    </div>
</template>

<script>
    import { Link } from '@inertiajs/vue3'
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';

    export default {
        components: { Link, Navbar, Sidebar },
        props: {
            student_number: String,
            full_name: String,
            position: String,
        },
    }
</script>

<style>
@import url(../../../css/standard.css);

.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
</style>