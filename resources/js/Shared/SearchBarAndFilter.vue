<template>
    <div class="row">
        <div class="col-2" :class="$style.filterDropDown">
            <input type="hidden" name="filter-type">
            <select class="form-select" :class="$style.filter" aria-label="Default select example" v-model="selectedOption">
                <option value="" disabled selected>Filter Search by</option>
                <option v-for="(option, index) in options" 
                        :key="index" 
                        :value="option.value">
                        {{ option.text }}
                </option>
            </select>
        </div>
        <div class="col-3">
            <input :class="$style.searchbar" type="text" :placeholder="'Search by '+selectedOption+'..'" v-model="searchQuery">
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            options: {
                type: Array,
                required: true
            }
        },
        data() {
            return {
                selectedOption: '',
                searchQuery: ''
            }
        },
        watch: {
            selectedOption(newVal, oldVal) {
                this.$emit('filter-changed', { option: newVal, query: this.searchQuery });
            },
            searchQuery(newVal, oldVal) {
                this.$emit('filter-changed', { option: this.selectedOption, query: newVal });
            }
        }
    }
</script>

<style module>
    .searchbar  {
        width: 100%;
        margin-left: -3%;
        padding: 7px;
        border-radius: 8px;
        outline: none;
        border: 1px solid rgba(40, 40, 40, 0.25);

        transition: border 0.15s ease-out;
    }

    .searchbar:focus {
        border: 1px solid rgba(13, 13, 13, 0.561)
    }

    .filter{
        margin-left: -5%;
        width: 100%;
        height: 40px;
        border-radius: 8px;
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .filterDropDown{
        margin-left: 1%;
    }
</style>