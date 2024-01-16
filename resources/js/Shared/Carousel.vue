<template>
    <div ref="carousel" id="carouselExampleIndicators" class="carousel slide">
        <div class="carousel-indicators">
            <button type="button" v-for="(image, index) in images" 
                data-bs-target="#carouselExampleIndicators"
                :data-bs-slide-to="index" 
                :class="{ active: index === 0 }" 
                :key="index"
                :aria-label="'Slide ' + (index + 1)">
            </button>
        </div>

        <div class="carousel-inner">
            <div class="carousel-item" :class="{ active: index === 0 }" v-for="(image, index) in images" :key="index">
                <img :src="image.url" class="d-block w-100" alt="...">
            </div>
        </div>
        <template v-if="images.length > 1">
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev" @click="prevSlide">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next" @click="nextSlide">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </template>
    </div>
</template>

<style scoped>
    .carousel-inner{
        margin: 4% 0%;
    }

    .carousel-item{
        height: 500px;
        background-color: #800000;
    }

    .carousel-item img {
        width: 100%;
        height: 100%;
        object-fit: contain; /* This makes the image scale while maintaining its aspect ratio */
    }
</style>
  
<script>
import { Carousel } from 'bootstrap'

export default {
    data() {
        return {
            mounted: false,
        }
    },
    props: {
        images: {
            type: Array,
            required: true
        },
        interval: {
            type: Number,
            default: 3000
        },
    },
    mounted() {
        this.carousel = new Carousel(this.$refs.carousel, {
            interval: this.interval,
            ride: 'carousel'
        })
    },
    methods: {
        prevSlide(){
                if (this.currentIndex > 0){
                    this.currentIndex--;
                }
                else {
                    this.currentIndex = this.images.length - 1;
                }
            },
        nextSlide(){
            if(this.currentIndex < this.images.length - 1){
                this.currentIndex++;
            }
            else {
                this.currentIndex = 0;
            }
        },
    }
}
</script>
  