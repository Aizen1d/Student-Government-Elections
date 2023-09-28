<template>
    <table class="my-table table-responsive">
        <thead class="my-thead head">
            <tr>
                <th class="my-cell" v-for="(column, index) in columns" :key="index">{{ column }}</th>
                <th style="width: 17px;"></th> <!-- Add this line -->
            </tr>
        </thead>
        <tbody class="my-tbody" :style="{ 'max-height':tableHeight }">
            <slot></slot> <!-- This slot will be replaced by the content inserted from the child component -->
        </tbody>
    </table>
</template>
  
<script>
    export default {
        props: {
            columns: {
                type: Array,
                required: true
            },
            tableHeight: {
                type: String,
                required: false,
                default: '180px'
            }
        }
    }
</script>
  
<style>
    .my-table {
        font-size: 18px;
        font-family: Arial, sans-serif;
        border-collapse: collapse;
    }

    .my-cell {
        border: none;
        text-align: center;
        padding: 10px;
    }

    .my-tbody th,
    .my-tbody td {
        font-weight: normal;
    }

    .my-tbody tr:hover:not(.active-row) {
        cursor: pointer;
        background-color: #d9ecf3;
    }

    .my-tbody {
        display: block;
        overflow-y: auto;
    }

    .my-thead,
    .my-tbody tr {
        display: table;
        width: 100%;
        table-layout: fixed;
    }

    .my-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .my-table tr:nth-child(odd) {
        background-color: white;
    }

    .my-table thead tr {
        color: #ffffff;
        background-color: #B90321 !important;
    }

    .active-row {
        background-color: #b1dceb !important;
        /* Change this to your desired color */
    }
</style>
  