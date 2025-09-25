<template>
  <v-card>
    <PerspectiveFilter 
      v-if="project.perspective"
      :perspective-id="project.perspective"
      @filter="handleFilter"
    />
    <ReportTable 
      :project-id="projectId" 
      :filters="activeFilters"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ReportTable from '~/components/report/ReportTable.vue'
import PerspectiveFilter from '~/components/report/PerspectiveFilter.vue'
import { Project } from '~/domain/models/project/project'

export default Vue.extend({
  components: {
    ReportTable,
    PerspectiveFilter
  },

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  data() {
    return {
      project: {} as Project,
      activeFilters: {} as Record<number, any>
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    }
  },

  async mounted() {
    await this.loadProject()
  },

  methods: {
    async loadProject() {
      this.project = await this.$repositories.project.findById(this.projectId)
    },

    handleFilter(filters: Record<number, any>) {
      this.activeFilters = filters
      // The ReportTable component will react to the filters prop change
    }
  }
})
</script>
