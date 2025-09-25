<template>
  <v-card>
    <v-card-title v-if="isProjectAdmin">
      <action-menu
        @upload="$router.push('dataset/import')"
        @download="$router.push('dataset/export')"
        @assign="dialogAssignment = true"
        @reset="dialogReset = true"
        @block="dialogBlock = true"
        @filter="showFilters = true"
      />
      
      <!-- Active Filters Display -->
      <div class="active-filters" v-if="activeFilters.length > 0">
        <v-chip
          v-for="(filter, index) in activeFilters"
          :key="index"
          class="ma-1"
        >
          <template v-if="filter.type === 'label'">
            Label: {{ 
              filter.value === 'agreement' ? 'Agreement' : 
              filter.value === 'disagreement' ? 'Disagreement' : 
              filter.labelName || getLabelName(filter.value)
            }}
          </template>
          <template v-else>
            {{ filter.perspective || filter.itemName }}: 
            {{ filter.value || (filter.min && filter.max ? 
            `${filter.min}-${filter.max}` : filter.min || filter.max || '') }}
          </template>
        </v-chip>
        <v-chip class="ma-1" color="primary">
          Mode: {{ 
            filterMode === 'every' ? 'All match' : 
            filterMode === 'some' ? 'Any match' : 
            'Majority match' 
          }}
        </v-chip>
        <v-btn text color="error" @click="resetFilters">Reset Filters</v-btn>
      </div>

      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        color="warning"
        @click.stop="dialogBlock = true"
      >
        Lock
      </v-btn>
      <v-spacer />
      <v-btn
        :disabled="!item.count"
        class="text-capitalize"
        color="error"
        @click="dialogDeleteAll = true"
      >
        {{ $t('generic.deleteAll') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          :item-key="itemKey"
          @cancel="dialogDelete = false"
          @remove="remove"
        />
      </v-dialog>
      <v-dialog v-model="dialogDeleteAll">
        <form-delete-bulk @cancel="dialogDeleteAll = false" @remove="removeAll" />
      </v-dialog>
      <v-dialog v-model="dialogAssignment">
        <form-assignment @assigned="assigned" @cancel="dialogAssignment = false" />
      </v-dialog>
      <v-dialog v-model="dialogReset">
        <form-reset-assignment @cancel="dialogReset = false" @reset="resetAssignment" />
      </v-dialog>
      <v-dialog v-model="dialogBlock">
        <form-block
          :selected="selected"
          @cancel="dialogBlock = false"
          @block="block"
        />
      </v-dialog>
      <v-dialog v-model="showFilters" max-width="800px">
        <example-filters
          ref="exampleFilters"
          :project-id="projectId"
          :labels="labels"
          @apply-filters="handleAppliedFilters"
          @cancel="showFilters = false"
        />
      </v-dialog>
    </v-card-title>
    <image-list
      v-if="project.isImageProject"
      v-model="selected"
      :items="filteredItems"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="filteredItems.length"
      :project-id="projectId"
      @update:query="updateQuery"
      @click:labeling="movePage"
      @assign="assign"
      @unassign="unassign"
    />
    <audio-list
      v-else-if="project.isAudioProject"
      v-model="selected"
      :items="filteredItems"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="filteredItems.length"
      :project-id="projectId"
      @update:query="updateQuery"
      @click:labeling="movePage"
      @assign="assign"
      @unassign="unassign"
    />
    <document-list
      v-else
      v-model="selected"
      :items="filteredItems"
      :is-admin="user.isProjectAdmin"
      :is-loading="isLoading"
      :members="members"
      :total="filteredItems.length"
      :project-id="projectId"
      :member-stats="cachedMemberStats"
      :labels="labels"                  
      @update:query="updateQuery"
      @click:labeling="movePage"
      @edit="editItem"
      @assign="assign"
      @unassign="unassign"
      @discrepancies="openDiscrepanciesChat"
    />

    <v-dialog v-model="showDiscrepanciesChatDialog" max-width="800">
      <discrepancies-chat 
        v-if="showDiscrepanciesChatDialog"
        :example="selectedExample"
        :projectId="projectId"
        @close="showDiscrepanciesChatDialog = false"
      />
    </v-dialog>

  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import { mapGetters } from 'vuex'
import Vue from 'vue'
import { NuxtAppOptions } from '@nuxt/types'
import DocumentList from '@/components/example/DocumentList.vue'
import FormAssignment from '~/components/example/FormAssignment.vue'
import FormDelete from '@/components/example/FormDelete.vue'
import FormDeleteBulk from '@/components/example/FormDeleteBulk.vue'
import FormResetAssignment from '~/components/example/FormResetAssignment.vue'
import ActionMenu from '~/components/example/ActionMenu.vue'
import AudioList from '~/components/example/AudioList.vue'
import ImageList from '~/components/example/ImageList.vue'
import FormBlock from '~/components/example/FormBlock.vue'
import DiscrepanciesChat from '@/components/example/DiscrepanciesChat.vue'
import ExampleFilters from '~/components/example/ExampleFilters.vue'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'
import { ExampleDTO, ExampleListDTO } from '~/services/application/example/exampleData'
import { MemberItem } from '~/domain/models/member/member'
import { LabelDTO } from '~/services/application/label/labelData'
import { APIMemberRepository } from '~/repositories/member/apiMemberRepository'

export default Vue.extend({
  components: {
    ActionMenu,
    AudioList,
    DocumentList,
    ImageList,
    FormAssignment,
    FormDelete,
    FormDeleteBulk,
    FormResetAssignment,
    FormBlock,
    ExampleFilters,
    DiscrepanciesChat
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query }: NuxtAppOptions) {
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  },

  data() {
    return {
      dialogDelete: false,
      dialogDeleteAll: false,
      dialogAssignment: false,
      dialogReset: false,
      item: {} as ExampleListDTO,
      selected: [] as ExampleDTO[],
      members: [] as MemberItem[],
      user: {} as MemberItem,
      showDiscrepanciesChatDialog: false,
      selectedExample: null as ExampleDTO | null,
      isLoading: false,
      isProjectAdmin: false,
      dialogBlock: false,
      showFilters: false,
      filteredItems: [] as ExampleDTO[],
      labels: [] as LabelDTO[],
      cachedMemberStats: {} as Record<string, { percentage: number, topLabel?: number }>,
      memberStats: {} as Record<string, { percentage: number, topLabel?: number }>,
      perspectiveStats: {} as Record<string, any>,
      activeFilters: [] as Array<{
        type: 'label' | 'perspective'
        value: any
        perspective?: string
      }>,
    }
  },

  async fetch() {
    this.isLoading = true
    const response = await this.$services.example.list(this.projectId, this.$route.query)
    
    this.item = response
    this.filteredItems = response.items
    
    this.user = await this.$repositories.member.fetchMyRole(this.projectId)
    if (this.user.isProjectAdmin) {
      this.members = await this.$repositories.member.list(this.projectId)
    }
    
    const labelService = this.getLabelService()
    if (labelService) {
      this.labels = await labelService.list(this.projectId)
    }
    
    // Cachear os resultados
    this.cachedMemberStats = await this.fetchMemberStats(this.item.items)
    this.memberStats = this.cachedMemberStats
    
    this.isLoading = false
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    itemKey(): string {
      if (this.project.isImageProject || this.project.isAudioProject) {
        return 'filename'
      } else {
        return 'text'
      }
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.projectId)
    this.isProjectAdmin = member.isProjectAdmin
  },

  methods: {
    openDiscrepanciesChat(item: ExampleDTO) {
      this.selectedExample = item
      this.showDiscrepanciesChatDialog = true
    },

    async handleAppliedFilters({ status, filters, queryParams, filterMode }: { 
      status: string, 
      filters: any[],
      queryParams: Record<string, string>,
      filterMode: 'every' | 'some' | 'majority'
    }) {
      try {
        this.isLoading = true
        this.filterMode = filterMode // Store the current filter mode
        
        const filteredMemberIds = 
          await this.$repositories.perspective
          .filterMembers(this.projectId, queryParams)

        this.activeFilters = filters.map(filter => {
          if (filter.type === 'label') {
            return {
              type: 'label',
              value: filter.value
            }
          } else {
            return {
              type: 'perspective',
              perspective: filter.itemName,
              value: filter.value || (filter.min && filter.max ? 
              `${filter.min}-${filter.max}` : filter.min || filter.max || '')
            }
          }
        })
        
        this.filteredItems = this.item.items.filter(item => {
          // Status filter
          if (status === 'locked' && !item.blocked) return false
          if (status === 'unlocked' && item.blocked) return false
          
          // Perspective filters (member-based)
          const hasPerspectiveFilters = filters.some(f => f.type === 'perspective')
          if (hasPerspectiveFilters) {
            if (filteredMemberIds.length === 0) return false

            const exampleAssigneeIds = item.assignments?.map(a => a.assignee_id) || []
            const totalAssignees = exampleAssigneeIds.length
            
            if (this.filterMode === 'every') {
              const allAssigneesFiltered = exampleAssigneeIds.every(assigneeId =>
                filteredMemberIds.includes(assigneeId))
              if (!allAssigneesFiltered) return false
            } 
            else if (this.filterMode === 'some') {
              const someAssigneeFiltered = exampleAssigneeIds.some(assigneeId =>
                filteredMemberIds.includes(assigneeId))
              if (!someAssigneeFiltered) return false
            }
            else if (this.filterMode === 'majority') {
              const matchingAssignees = exampleAssigneeIds.filter(assigneeId =>
                filteredMemberIds.includes(assigneeId)).length
              
              // Calculate simple majority (more than half)
              const majorityThreshold = Math.floor(totalAssignees / 2) + 1
              if (matchingAssignees < majorityThreshold) return false
            }
          }
          
          // Label filters
          const labelFilters = filters.filter(f => f.type === 'label')
          if (labelFilters.length > 0) {
            const itemStats = this.memberStats[item.id]
            
            for (const filter of labelFilters) {
              if (filter.value === 'agreement') {
                if (!itemStats?.topLabel) return false
              } else if (filter.value === 'disagreement') {
                if (itemStats?.topLabel !== undefined) return false
              } else if (typeof filter.value === 'number') {
                if (itemStats?.topLabel !== filter.value) return false
              }
            }
          }
          
          return true
        })
      } catch (error) {
        console.error('Error filtering:', error)
        this.filteredItems = [...this.item.items]
        this.activeFilters = []
      } finally {
        this.isLoading = false
      }
    },

    async block(blocked: boolean) {
      const exampleIds = this.selected.map(example => example.id)
      await this.$services.example.bulkUpdateBlockedStatus(this.projectId, exampleIds, blocked)
      this.$fetch()
      this.dialogBlock = false
      this.selected = []
    },
    
    async remove() {
      await this.$services.example.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    async removeAll() {
      await this.$services.example.bulkDelete(this.projectId, [])
      this.$fetch()
      this.dialogDeleteAll = false
      this.selected = []
    },

    updateQuery(query: object) {
      this.$router.push(query)
    },

    movePage(query: object) {
      const link = getLinkToAnnotationPage(this.projectId, this.project.projectType)
      this.updateQuery({
        path: this.localePath(link),
        query
      })
    },

    editItem(item: ExampleDTO) {
      this.$router.push(`dataset/${item.id}/edit`)
    },

    async assign(exampleId: number, userId: number) {
      await this.$repositories.assignment.assign(this.projectId, exampleId, userId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async unassign(assignmentId: string) {
      await this.$repositories.assignment.unassign(this.projectId, assignmentId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async assigned() {
      this.dialogAssignment = false
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async resetAssignment() {
      this.dialogReset = false
      await this.$repositories.assignment.reset(this.projectId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    applyFiltersToItems(items: ExampleDTO[], filters: any[]) {
      if (filters.length === 0) return items
      
      return items.filter(item => {
        for (const filter of filters) {
          if (filter.type === 'label') {
            if (filter.value === 'agreement') {
              if (this.getLabelAgreementStatus(item) !== 'agreement') return false
            } else if (filter.value === -1) {
              if (this.getLabelAgreementStatus(item) !== 'disagreement') return false
            } else if (this.memberStats[item.id]?.topLabel !== filter.value) {
              return false
            }
          } else if (filter.type === 'perspective') {
            const perspectiveData = 
            this.perspectiveStats[item.id]?.statistics?.[filter.perspective]
            
            if (!perspectiveData) return false
            
            if (filter.value === 'agreement') {
              if (!this.hasPerspectiveAgreement(perspectiveData)) return false
            } else {
              if (perspectiveData[filter.value] === undefined) return false
              if (perspectiveData[filter.value] <= 0) return false
              
              const total = 
              Object.values(perspectiveData).reduce((sum: number, val: any) => sum + val, 0)
              if (total === 0) return false
              
              const values = Object.values(perspectiveData) as number[]
              const max = Math.max(...values)
              
              if (perspectiveData[filter.value] !== max) return false
              
              const percentage = (max / total) * 100
              if (percentage < this.project.agreementPercentage) return false
            }
          }
        }
        return true
      })
    },

    addFilter(filter: { type: 'label' | 'perspective'; value: any; perspective?: string }) {
      const exists = this.activeFilters.some(f => 
        f.type === filter.type && 
        f.value === filter.value && 
        f.perspective === filter.perspective
      )
      
      if (!exists) {
        this.activeFilters.push(filter)
        this.filteredItems = this.applyFiltersToItems(this.item.items, this.activeFilters)
      }
    },

    removeFilter(index: number) {
      this.activeFilters.splice(index, 1)
      this.filteredItems = this.applyFiltersToItems(this.item.items, this.activeFilters)
    },

    resetFilters() {
      this.activeFilters = []
      this.filteredItems = this.item.items
      
      // Reset the ExampleFilters component's internal state
      if (this.$refs.exampleFilters) {
        this.$refs.exampleFilters.resetFilters()
      }
    },

    getLabelAgreementStatus(item: ExampleDTO): string {
      if (!item.blocked) return 'discussion'
      if (this.memberStats[item.id]?.topLabel === undefined) return 'disagreement'
      return 'agreement'
    },

    hasPerspectiveAgreement(perspectiveData: any): boolean {
      if (!perspectiveData) return false
      
      const values = Object.values(perspectiveData) as number[]
      const total = values.reduce((sum, val) => sum + val, 0)
      if (total === 0) return false
      
      const max = Math.max(...values)
      const maxCountOccurrences = values.filter(v => v === max).length
      
      return maxCountOccurrences === 1 && (max / total) * 100 >= this.project.agreementPercentage
    },

    getLabelName(labelId: number): string {
      if (labelId === -1) return 'Disagreement'
      if (labelId === 'agreement') return 'Agreement'
      const label = this.labels.find(l => l.id === labelId)
      return label?.text || `Label ${labelId}`
    },

    async fetchMemberStats(items: ExampleDTO[]) {
      const stats: Record<string, { percentage: number, topLabel?: number }> = {}
      const repository = new APIMemberRepository()
      
      for (const example of items) {
        try {
          const membersWithLabels = await repository.fetchMembersWithLabels(
            this.projectId,
            example.id
          )
          
          const { agreementPercentage, topLabel } = 
            this.calculateExampleAgreement(membersWithLabels)
          stats[example.id] = { 
            percentage: agreementPercentage,
            topLabel 
          }
        } catch (error) {
          console.error(`Error processing example ${example.id}:`, error)
          stats[example.id] = { percentage: 0 }
        }
      }
      
      return stats
    },
    
    
    calculateExampleAgreement(membersWithLabels: Array<{ labels: number[] }>) {
      if (!membersWithLabels || membersWithLabels.length === 0) {
        return { agreementPercentage: 0, topLabel: undefined }
      }

      const labelCounts = new Map<number, number>()
      membersWithLabels.forEach(member => {
        member.labels?.forEach(labelId => {
          labelCounts.set(labelId, (labelCounts.get(labelId) || 0) + 1)
        })
      })

      let topLabels: number[] = []
      let maxCount = 0
      
      labelCounts.forEach((count, labelId) => {
        if (count > maxCount) {
          maxCount = count
          topLabels = [labelId]
        } else if (count === maxCount) {
          topLabels.push(labelId)
        }
      })

      const agreementPercentage = (maxCount / membersWithLabels.length) * 100
      const topLabel = topLabels.length === 1 ? topLabels[0] : undefined
      
      return { agreementPercentage, topLabel }
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
    }
  }
})
</script>

<style scoped>
.active-filters {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  margin-left: 12px;
}

::v-deep .v-dialog {
  width: 800px;
}
</style>