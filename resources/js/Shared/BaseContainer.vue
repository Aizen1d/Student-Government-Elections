<template>
    <div :class="$style.container">
        <slot></slot>
    </div>
</template>

<style module>
    .container{
        margin-top: 1.5%;
        background-color: white;
        margin: 1.5% -1% 0% -1%;
        padding: 30px 30px 20px 30px;
        border-radius: 7px;
    }

    .container {
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.07), 0 6px 20px 0 rgba(0, 0, 0, 0.08);
    }
</style>