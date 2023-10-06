<template>
    <div :class="$style.dropzone" @drop.prevent="onDrop" @dragenter.prevent @dragover.prevent>

        <!-- Add a loading spinner -->
        <div v-if="isLoadingAttachments" class="d-flex justify-content-center" :class="$style.loading">
            <div class="spinner-border" role="status"></div>
            <span class="sr-only my-2">Retrieving files..</span>
        </div>

        <div :class="$style.dragDropDefaultContainer" v-if="!attachments.length && !isLoadingAttachments">
            <img src="../../images/icons/insert_data.svg" alt="" height="30" width="30">
            <span>Drag and drop your files here</span>
        </div>

        <div :class="$style.dragDropFilesContainer" v-if="attachments.length && !isLoadingAttachments">
            <div v-for="(file, index) in attachments" :key="index" :class="$style.fileList">
                <span> 
                    <a :class="$style.fileItem" :href="file.url" target="_blank" style="color: black;"> {{ file.name }} </a>
                    <button type="button" :class="$style.removeAttachment" :disabled="saving || updating"
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
        acceptedFileTypes: String,
        notAcceptedMessage: String,
        isLoadingAttachments: Boolean,
        saving: Boolean,
        updating: Boolean,
        fileSize: Number,
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

                if (file.size > this.fileSize * 1024 * 1024) {
                    alert(file.name + ' is larger than ' + String(this.fileSize) + ' MB, please upload a smaller file');
                    continue;
                }

                let acceptedTypes = this.acceptedFileTypes.split(',');
                if (!acceptedTypes.includes(file.type)) {
                    alert(file.name + ' is not an accepted file type, ' + this.notAcceptedMessage);
                    continue;
                }

                /*if (!this.acceptedFileTypes.includes(file.type)) {
                    alert(file.name + ' is not an accepted file type, please upload a ' + this.acceptedFileTypes + ' file');
                    continue;
                }*/

                // Create a new object URL for the file
                let url = URL.createObjectURL(file);

                // Check if the file is already in the list of files
                // If it is, then do not add it again
                if (!this.attachments.some(existingFile => existingFile.name === file.name)) {
                    this.attachments.push({ file:file, 
                                            name: file.name, 
                                            url: url 
                                        });
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
.loading{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;
}
.dropzone {
    width: 100%;
    height: 200px;
    background-color: rgb(243, 243, 243);
    border: 2px dashed rgb(205, 205, 205);
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

.fileItem {
    text-decoration: none;
}
.fileItem:hover{
    text-decoration: underline;
    cursor: pointer;
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
    margin-left: 2%;
    background-color: #B90321;
    color: white;
    width: 30px;
    border-radius: 8px;
    outline: none;
    border: none;
}

.removeAttachment:hover{
    background-color: #b20522;
}
</style>
  