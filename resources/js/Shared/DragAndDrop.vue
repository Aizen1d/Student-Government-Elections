<template>
    <div :class="$style.dropzone" @drop.prevent="onDrop" @dragenter.prevent @dragover.prevent>

        <div :class="$style.dragDropDefaultContainer" v-if="!attachments.length">
            <img src="../../images/icons/insert_data.svg" alt="" height="30" width="30">
            <span>Drag and drop your files here</span>
        </div>

        <div :class="$style.dragDropFilesContainer" v-if="attachments.length">
            <div v-for="(file, index) in attachments" :key="index" :class="$style.fileList">
                <span> {{ file.name }} 
                    <button type="button" :class="$style.removeAttachment"
                        @click="removeFile(index)">X
                    </button>
                </span>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        modelValue: Array,
        acceptedFileTypes: String
    },
    computed: {
        attachments: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit('update:modelValue', value);
            }
        }
    },
    methods: {
        addFiles(files) {
            // Add the files to the list of files
            for (let i = 0; i < files.length; i++) {
                let file = files[i];

                // Check if a file is of an accepted type
                if (!file.type.startsWith(this.acceptedFileTypes)) {
                    alert(file.name + ' is not an accepted file type, please upload a ' + this.acceptedFileTypes + ' file');
                    continue;
                }

                // Check if the file is already in the list of files
                // If it is, then do not add it again
                if (!this.attachments.some(existingFile => existingFile.name === file.name)) {
                    this.attachments.push(file);
                }
            }
        },
        onDrop(event) {
            event.preventDefault();
            this.addFiles(event.dataTransfer.files);
        },
        removeFile(index) {
            // Handle file removal
            this.attachments.splice(index, 1);
        },
    },
};
</script>

<style module>
.dropzone {
    width: 100%;
    height: 200px;
    background-color: #e0e0e0;
    border-radius: 10px;
}

.dragDropDefaultContainer {
    display: flex;
    flex-direction: column;
    /* Stacks items vertically */
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 100%;
    width: 100%;
}

.dragDropFilesContainer {
    display: grid;
    align-content: start;
    justify-items: start;

    max-height: 200px;
    height: 100%;
    width: 100%;

    overflow-y: auto;
    overflow-x: hidden;
}

.fileList {
    display: flex;
    justify-content: space-between;
    width: 100%;

    margin-top: 2%;
    margin-left: 3%;
}

.fileList span {
    word-wrap: break-word;
    width: 90%;
}

.removeAttachment {
    background-color: #B90321;
    color: white;
    width: 30px;
    border-radius: 8px;
    outline: none;
    border: none;
}
</style>
  