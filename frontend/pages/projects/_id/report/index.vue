<template>
  <v-card>
    <v-card-actions>
      <v-btn 
        color="primary" 
        @click="showReportDialog = true"
        :loading="loadingReport"
      >
        Show Report
      </v-btn>
    </v-card-actions>

    <v-dialog
      v-model="showReportDialog"
      max-width="1200"
      persistent
    >
      <ReportTable 
        v-if="showReportDialog"
        :project-id="projectId" 
        @close="showReportDialog = false" 
      />
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ReportTable from '~/components/report/ReportTable.vue'

export default Vue.extend({
  components: {
    ReportTable
  },

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  data() {
    return {
      showReportDialog: false,
      loadingReport: false
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    }
  }
})
</script>
