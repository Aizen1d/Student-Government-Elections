<template>
    <div style="position: relative; display: inline-block;">
    
        <div v-show="showInfo" style="padding: 3px 3px; background-color: rgb(36, 36, 36); position: absolute; left: 140%; top: 50%; transform: translateY(-50%); border: white 1px solid; border-top-left-radius: 7px; border-bottom-left-radius: 7px; max-width: fit-content;">
            <p v-show="showInfo" class="tool" style="text-align: justify;">
                <slot></slot>
            </p>
            <div v-show="showInfo" class="tooltip-arrow"></div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                showInfo: true
            }
        }
    }
</script>

<style scoped>
    .tooltip-arrow {
        width: 0;
        height: 0;
        border-top: 7px solid transparent;
        border-bottom: 7px solid transparent;
        border-right: 7px solid rgb(36, 36, 36);
        position: absolute;
        top: 50%;
        left: -6px;
        transform: translateY(-50%);
    }

    .tool {
        color: white;
        font-size: 12px;
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 5px;
        word-wrap: break-word; /* Enable word wrapping */
        max-width: 350px; /* Optional: Set a maximum width for the tooltip */
    }
</style>