<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="container">
        <h1>Insert Data</h1>
        <p>Student Number: {{ FullName }}</p>
        <p>Position: {{ Position }}</p>
    </div>
</template>

<script setup>
    import { Link } from '@inertiajs/vue3'
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import { defineComponent } from 'vue';

    const comp = defineComponent({
        components: { Link, Navbar, Sidebar }, 
        props: {
            FullName: String,
            Position: String,
        },
    });
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