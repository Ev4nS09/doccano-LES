<template>
  <v-container>
    <v-card-title>
      <action-menu @export="handleExport" />
    </v-card-title>

    <v-row>
      <v-col cols="12">
        <statistics-overview 
          :project-id="projectId" 
          :stats="generalStats"
        />
      </v-col>
    </v-row>

    <v-card-title class="d-flex align-center">
      <v-btn color="primary text-capitalize" @click="showPerspectiveFilters = true" class="mr-4">
        Filter by Perspective
      </v-btn>
      
      <div v-if="activePerspectiveFilters.length > 0" class="d-flex align-center">
        <span class="mr-2">Active Filters:</span>
        <v-chip
          v-for="(filter, index) in activePerspectiveFilters"
          :key="index"
          class="ma-1"
        >
          {{ getFilterDisplayText(filter) }}
        </v-chip>
        <v-btn text color="error" @click="resetFilters" class="ml-2">Reset Filters</v-btn>
      </div>
    </v-card-title>

    <v-dialog v-model="showPerspectiveFilters" max-width="800px">
      <PerspectiveFilters
        ref="perspectiveFilters"
        :project-id="projectId"
        @apply-filters="handlePerspectiveFilters"
        @cancel="showPerspectiveFilters = false"
      />
    </v-dialog>

    <v-row>
      <v-col cols="12">
        <v-alert
          v-if="examples.length === 0"
          type="warning"
          prominent
          border="left"
        >
          <v-icon left>mdi-alert</v-icon>
          This project doesn't have any examples yet.
        </v-alert>

        <v-alert
          v-else-if="selectedExamples.length === 0 
          && activePerspectiveFilters.length > 0"
          type="info"
          prominent
          border="left"
        >
          <v-icon left>mdi-filter</v-icon>
          No examples match the current filters. Try adjusting your perspective filters.
        </v-alert>

        <v-alert
          v-else-if="selectedExamples.length === 0"
          type="info"
          prominent
          border="left"
        >
          <v-icon left>mdi-information</v-icon>
          No examples available with the current perspective configuration.
        </v-alert>

        <perspective-distribution 
          v-else
          ref="perspectiveDistribution"
          :project-id="projectId"
          :example-stats="exampleStats"
          :examples="selectedExamples"
          :labels="labels"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import ActionMenu from '@/components/metrics/ActionMenu.vue'
import StatisticsOverview from '@/components/metrics/StatisticsOverview.vue'
import PerspectiveDistribution from '@/components/metrics/PerspectiveDistribution.vue'
import PerspectiveFilters from '@/components/metrics/PerspectiveFilters.vue'

export default {
  components: {
    StatisticsOverview,
    PerspectiveDistribution,
    ActionMenu,
    PerspectiveFilters
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      generalStats: {
        totalExamples: 0,
        annotatedExamples: 0,
        participationRate: 0,
        fullParticipationRate: 0
      },
      totalMembers: 0,
      perspectiveItems: [],
      examples: [],
      selectedExamples: [],
      agreementPercentage: 50,
      loading: false,
      exampleStats: {},
      showPerspectiveFilters: false,
      activePerspectiveFilters: []
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    projectId() {
      return this.$route.params.id
    }
  },

  async created() {
    await this.loadData()
  },

  methods: {
    async handleExport(format = 'csv') {
      this.exporting = true;
      try {
        const perspectiveDistribution = this.$refs.perspectiveDistribution;
        if (!perspectiveDistribution) {
          throw new Error('Perspective distribution component not found');
        }
        
        const selectedItemsStats = perspectiveDistribution.getSelectedItemsStats();
        console.log(selectedItemsStats)
        
        if (!selectedItemsStats) {
          throw new Error('No statistics data available');
        }

        switch(format) {
          case 'csv':
            await this.$repositories.perspective.
            exportStatsAsCSV(this.generalStats, selectedItemsStats);
            break;
          case 'json':
            await this.$repositories.perspective.
            exportStatsAsJSON(this.generalStats, selectedItemsStats);
            break;
          case 'pdf':
            await this.$repositories.perspective.exportStatsAsPDF(
              this.generalStats, 
              selectedItemsStats, 
              this.projectId
            );
            break;
          default:
            throw new Error(`Unsupported export format: ${format}`);
        }
      } catch (error) {
        console.error('Export failed:', error);
        this.$toast.error(`Failed to export as ${format.toUpperCase()}: ${error.message}`);
      } finally {
        this.exporting = false;
      }
    },
    async loadData() {
      this.loading = true
      try {
        // Load all data in parallel
        const labelService = this.getLabelService()
        if (labelService) {
          this.labels = await labelService.list(this.projectId)
        }

        const [examplesResponse, members, agreementPercentage] = await Promise.all([
          this.$services.example.list(this.projectId, { limit: '1000' }),
          this.$repositories.member.listProjectMembers(this.projectId),
          this.$services.project.getAgreementPercentage(this.projectId)
        ])

        this.agreementPercentage = agreementPercentage || 50

        // Examples
        this.generalStats.totalExamples = examplesResponse.items.length || 0
        this.examples = examplesResponse.items.filter(item => item.blocked) || []
        this.generalStats.annotatedExamples = this.examples.length || 0
              
        const memberIds = members.map(member => member.id);

        // Members
        this.totalMembers = members.length || 0
              
        // Calculate general stats
        console.log("System Load")
        console.log(memberIds)
        await this.calculateStats(memberIds)
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        this.loading = false
      }
    },

    async calculateStats(validIds) {
      const exampleStats = {}
      const selectedExamples = []
      let totalParticipation = 0
      let fullParticipationCount = 0
      let totalExamples = 0

      for (const example of this.examples) {
        console.log("System Debug:")
        console.log(example.id)
        // Todos os membros do exemplo com as labels que atribuiram
        const membersWithLabels = 
        await this.$repositories.member.fetchMembersWithLabels(this.projectId, example.id)

        console.log(membersWithLabels)
        // Todos os membros do exemplo que atribuiram labels
        let validMembers = membersWithLabels.filter(m => m.labels.length > 0)
        console.log(validMembers)

        // Todos os membros do exemplo que atribuiram labels e correspondem à perspetiva selecionada
        validMembers = validMembers.filter(m => validIds.includes(m.member_id));
        console.log(validMembers)
        
        // Todos os membros do exemplo com ou sem labels e correspondem à perspetiva selecionada
        console.log(validIds)

        const membersWithLabelsAndPerspective = membersWithLabels.filter(
          m => validIds.includes(m.member_id)) 
        
        console.log("-----")
        console.log(membersWithLabelsAndPerspective)

        const totalValid = validMembers.length

        // Se não houver nenhum membro com label atribuida e com a perspetiva selecionada ignora
        if(membersWithLabelsAndPerspective.length === 0) continue
        totalExamples++

        // --- Participação ---
        const participationRatio = totalValid / membersWithLabelsAndPerspective.length
        totalParticipation += participationRatio

        if (totalValid === membersWithLabelsAndPerspective.length) {
          fullParticipationCount++
        }

        // Se nenhum dos membros com a perspetiva selecionada atribuiu labels, não conta 
        // (Conta apenas para participação)
        if (totalValid === 0) continue
        selectedExamples.push(example)


        // --- Rótulos ---
        if (totalValid > 0) {
          const labelCounts = {}

          for (const member of validMembers) {
            for (const labelId of member.labels) {
              labelCounts[labelId] = (labelCounts[labelId] || 0) + 1
            }
          }

          const labelPercentages = {}
          for (const labelId in labelCounts) {
            labelPercentages[labelId] = Math.round((labelCounts[labelId] / totalValid) * 100)
          }

          console.log(labelPercentages)
          console.log(validMembers)
          exampleStats[example.id] = labelPercentages
        }
      }
      this.selectedExamples = selectedExamples

      this.exampleStats = exampleStats
      this.generalStats.participationRate = totalExamples > 0
        ? Math.round((totalParticipation / totalExamples) * 100)
        : 0

      this.generalStats.fullParticipationRate = totalExamples > 0
        ? Math.round((fullParticipationCount / totalExamples) * 100)
        : 0
      
    },
    getLabelService() {
      if (!this.project) return null
      
      if (this.project.projectType === 'IntentDetectionAndSlotFilling') {
        return this.$services.categoryType
      } else if (this.project.useRelation) {
        return this.$services.spanType
      } else if (this.project.canDefineCategory) {
        return this.$services.categoryType
      } else {
        return this.$services.spanType
      }
    },
    handlePerspectiveFilters({ queryParams, filters }) {
      this.activePerspectiveFilters = filters
      this.perspectiveQueryParams = queryParams
      this.showPerspectiveFilters = false
      this.refreshStatistics()
    },
    async refreshStatistics() {
      const filteredMemberIds = await this.$repositories.perspective
        .filterMembers(this.projectId, this.perspectiveQueryParams)
      
      const projectMembers = 
      await this.$repositories.member.listProjectMembers(this.projectId)
      
      // Create a mapping of user IDs to member IDs
      const userToMemberMap = {}
      projectMembers.forEach(member => {
        userToMemberMap[member.user] = member.id
      })
      
      // Convert filtered user IDs to member IDs
      const memberIdsToCalculate = filteredMemberIds
        .map(userId => userToMemberMap[userId])
        .filter(id => id !== undefined) // Filter out any undefined mappings
      
      this.calculateStats(memberIdsToCalculate)
    },
    getFilterDisplayText(filter) {
      if (!filter.itemName) return 'Invalid filter'

      if (this.isNumericType(filter.itemType)) {
        let text = `${filter.itemName}: `
        if (filter.min !== undefined) text += `min ${filter.min}`
        if (filter.min !== undefined && filter.max !== undefined) text += ' - '
        if (filter.max !== undefined) text += `max ${filter.max}`
        return text
      }

      return `${filter.itemName}: ${filter.value}`
    },

    isNumericType(type) {
      return type === 'int' || type === 'float'
    },

    resetFilters() {
      this.activePerspectiveFilters = []
      this.perspectiveQueryParams = {}
      this.selectedExamples = [...this.examples]
      
      if (this.$refs.perspectiveFilters) {
        this.$refs.perspectiveFilters.resetFilters()
      }
      
      this.refreshStatistics()
    },
  }
}
</script>
