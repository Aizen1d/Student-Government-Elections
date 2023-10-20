<template>
    <div class="skeleton-loader" v-if="loading">
        <div class="skeleton-item" v-for="index in itemCount" :key="index">
            <div class="skeleton-image"></div>
            <div class="skeleton-info">
                <p></p>
                <h1></h1>
            </div>
        </div>
    </div>
    <slot v-else></slot>
</template>
  
<script>
export default {
    name: 'SkeletonLoader',
    props: {
        loading: {
            type: Boolean,
            required: true,
        },
        itemCount: {
            type: Number,
            default: 1
        }
    }
}
</script>
  
<style scoped>
    @keyframes loading {
        0% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0 50%;
        }
    }

    .skeleton-loader {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin: 0% 5%;
    }

    .skeleton-item {
        width: 31.5%;
        margin-top: 2em;
        margin-bottom: 2em;
    }

    .skeleton-item .skeleton-image {
        width: 100%;
        height: 33vh;
        background: linear-gradient(90deg, #f0f0f0 25%, #d6d5d5 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 2s infinite;
    }

    .skeleton-item .skeleton-info {
        margin: 0% 2%;
    }

    .skeleton-item .skeleton-info h1 {
        height: 16px;
        /* Adjust based on your font size */
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 2s infinite;
    }
</style>
  