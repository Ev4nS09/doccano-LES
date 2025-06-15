<template>
    <v-card>
        <dataset-list/>
    </v-card>
</template>


<script lang="ts">
import Vue from 'vue'
import DatasetList from '@/components/discrepancies/DatasetList.vue'

export default Vue.extend({
  components: {
        DatasetList,
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],


  data() {
    return {
    }
  },

  computed: {
  },

  watch: {
  },

  methods: {
    async list() {
    },

    async remove() {
    },

    async download() {
    },

  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>




