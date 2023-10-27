<template>
    <button :class="$style.button">
       <slot></slot>
    </button>
</template>

<style module>
    .button{
        padding: 10px 50px 10px 50px;
        border: transparent;
        border-radius: 10px;
        background-color: #B90321;
        color: white;
        font-size: 17px;
        font-family: 'Source Sans Pro', sans-serif !important;
    }
    .button:hover{
        background-color: #a6021d;
    }
    .button:disabled{
        background-color: #cccccc;
    }

</style>