<template>
    <button :class="$style.button" @click="$emit('click')">
       <slot></slot>
    </button>
</template>

<style module>
   .button{
        padding: 10px 60px 10px 60px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
    }

    .button:disabled{
        background-color: #cccccc;
    }

    .button:hover{
        background-color: #a6021d;
    }
</style>