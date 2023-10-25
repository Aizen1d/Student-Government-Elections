<template>
    <div class="skeleton-loader" :style="{ margin: containerMargin }" v-if="loading">
        <div class="skeleton-item" :style="{ margin: itemMargin }"  v-for="index in itemCount" :key="index">
            <div class="skeleton-image" :style="{ width: imageWidth, height: imageHeight, borderRadius: borderRadius }"></div>
        </div>
    </div>
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
        },
        imageWidth: {
            type: String,
            default: '100%'
        },
        imageHeight: {
            type: String,
            default: '33vh'
        },
        containerMargin: {
            type: String,
            default: '0% 1%',
            required: false,
        },
        itemMargin: {
            type: String,
            default: '1em',
            required: false,
        },
        borderRadius: {
            type: String,
            default: '0px',
            required: false,
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
        justify-content: flex-start;
        flex-wrap: wrap;
    }

    .skeleton-item {
        width: 31.5%;
        margin-top: 2em;
        margin-bottom: 2em;
    }

    .skeleton-item .skeleton-image {
        background: linear-gradient(90deg, #f0f0f0 25%, #d6d5d5 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 2s infinite;
    }
</style>
  