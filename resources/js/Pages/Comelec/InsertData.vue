<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <h1>Insert Data</h1>
</template>

<script setup>
    import { Link } from '@inertiajs/vue3'
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import { defineComponent } from 'vue';

    const comp = defineComponent({
        components: { Link, Navbar, Sidebar }, 
    });
</script>

<style>
@import url(../../../css/standard.css);

</style>