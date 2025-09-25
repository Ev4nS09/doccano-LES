<template>
  <v-card class="pa-4">
    <v-card-title class="d-flex justify-space-between align-center">
      <span>Filter by Perspective and Labels</span>
      <v-btn icon @click="$emit('cancel')">
        <v-icon>{{ mdiClose }}</v-icon>
      </v-btn>
    </v-card-title>

    <v-divider></v-divider>

    <v-card-text>
      <v-row class="mb-4">
        <v-col cols="12" sm="6">
          <v-select
            v-model="statusFilter"
            :items="statusOptions"
            label="Example Status"
            outlined
            dense
          />
        </v-col>

        <v-col cols="12" sm="6">
          <v-select
            v-model="filterMode"
            :items="filterModeOptions"
            label="Filter Match Mode"
            outlined
            dense
          />
        </v-col>
      </v-row>

      <!-- Seção de filtros por label -->
      <v-row class="mb-4" v-if="statusFilter === 'locked'">
        <v-col cols="12">
          <v-select
            v-model="labelFilter"
            :items="combinedLabelOptions"
            label="Label Filter"
            outlined
            dense
            :loading="labelsLoading"
            :disabled="labels.length === 0"
          >
            <template #item="{ item }">
              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
                <v-list-item-subtitle v-if="item.id">ID: {{ item.id }}</v-list-item-subtitle>
              </v-list-item-content>
            </template>
            <template #no-data>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>No labels available</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-select>
        </v-col>
      </v-row>

      <v-row v-if="statusFilter === 'locked'">
        <v-col cols="5">
          <v-select
            v-model="newFilter.item"
            :items="items"
            label="Select Perspective"
            outlined
            dense
            item-text="name"
            item-value="id"
          />
        </v-col>

        <v-col cols="5">
          <template v-if="selectedItem">
            <!-- List -->
            <v-select
              v-if="selectedItem.item_type === 'list'"
              v-model="newFilter.value"
              :items="selectedItem.selection_list"
              label="Select Value"
              outlined
              dense
            />

            <!-- Boolean (Checkbox) -->
            <v-checkbox
              v-else-if="selectedItem.item_type === 'bool'"
              v-model="newFilter.value"
              :label="`Has ${selectedItem.name}`"
              :true-value="true"
              :false-value="false"
              dense
              hide-details
            />

            <!-- Numeric -->
            <template v-else-if="isNumericType(selectedItem.item_type)">
              <v-text-field
                v-model="newFilter.min"
                :label="`Min ${selectedItem.name}`"
                type="number"
                outlined
                dense
                class="mb-2"
              />
              <v-text-field
                v-model="newFilter.max"
                :label="`Max ${selectedItem.name}`"
                type="number"
                outlined
                dense
              />
            </template>

            <!-- Default (String) -->
            <v-text-field
              v-else
              v-model="newFilter.value"
              :label="`Value for ${selectedItem.name}`"
              outlined
              dense
            />
          </template>
        </v-col>

        <v-col cols="2" class="d-flex align-start">
          <v-btn
            color="primary"
            @click="addFilter"
            :disabled="!canAddFilter"
            block
          >
            <v-icon>{{ mdiPlus }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <div v-if="addedFilters.length > 0" class="mt-4">
        <v-subheader>Filters to be applied:</v-subheader>
        <v-chip
          v-for="(filter, index) in addedFilters"
          :key="index"
          close
          class="ma-1"
          @click:close="removeAddedFilter(index)"
        >
          {{ getFilterDisplayText(filter) }}
        </v-chip>
      </div>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="$emit('cancel')">Cancel</v-btn>
      <v-btn
        color="primary"
        @click="applyFilters"
        :disabled="addedFilters.length === 0 && statusFilter === 'all'"
      >
        Apply
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPlus, mdiClose } from '@mdi/js'
import { PerspectiveItem } from '@/domain/models/perspective/perspective'
import { APIPerspectiveRepository } from '@/repositories/perspective/apiPerspectiveRepository'
import { APIProjectRepository } from '@/repositories/project/apiProjectRepository'
import { LabelDTO } from '~/services/application/label/labelData'

type StatusFilter = 'all' | 'locked' | 'unlocked'

export default Vue.extend({
  props: {
    projectId: {
      type: String,
      required: true
    },
    labels: {
      type: Array as () => LabelDTO[],
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      mdiPlus,
      mdiClose,
      statusFilter: 'all' as StatusFilter,
      filterMode: 'every' as 'every' | 'some',
      statusOptions: [
        { text: 'All examples', value: 'all' },
        { text: 'Locked only', value: 'locked' },
        { text: 'Unlocked only', value: 'unlocked' }
      ],
      filterModeOptions: [
        { text: 'All assignees must match', value: 'every' },
        { text: 'At least one assignee matches', value: 'some' },
        { text: 'Majority of assignees match (>50%)', value: 'majority' }
      ],
      labelFilter: null as string | number | null,
      newFilter: {
        item: null as number | null,
        value: null as any,
        min: null as number | null,
        max: null as number | null
      },
      addedFilters: [] as Array<{
        item: number
        value?: any
        min?: number
        max?: number
        itemType: string
        itemName: string
      }>,
      items: [] as PerspectiveItem[],
      labelsLoading: false
    }
  },

  computed: {
    selectedItem(): PerspectiveItem | null {
      if (this.newFilter.item === null) return null
      return this.items.find(i => i.id === this.newFilter.item) || null
    },

    canAddFilter(): boolean {
      if (!this.selectedItem) return false
      if (this.isNumericType(this.selectedItem.item_type)) {
        return this.newFilter.min !== null || this.newFilter.max !== null
      }
      return this.newFilter.value !== null
    },

    combinedLabelOptions() {
      const baseOptions = [
        { text: 'No label filter', value: null },
        { text: 'Agreement', value: 'agreement' },
        { text: 'Disagreement', value: 'disagreement' }
      ]
      
      // Verifica se há labels disponíveis
      if (this.labels.length === 0) {
        return baseOptions
      }

      const labelOptions = this.labels.map(label => ({
        text: label.text,
        value: label.id,
        id: label.id
      }))

      return [...baseOptions, ...labelOptions]
    }
  },

  async created() {
    this.labelsLoading = true
    try {
      const apiProjectRepository = new APIProjectRepository()
      const perspective = await apiProjectRepository.getPerspective(this.projectId)

      const apiPerspectiveRepository = new APIPerspectiveRepository()
      this.items = await apiPerspectiveRepository.listPerspectiveItem(perspective)
    } finally {
      this.labelsLoading = false
    }
  },

  methods: {
    isNumericType(type: string): boolean {
      return type === 'int' || type === 'float'
    },

    getFilterDisplayText(filter: any): string {
      const item = this.items.find(i => i.id === filter.item)
      if (!item) return 'Invalid filter'

      if (this.isNumericType(filter.itemType)) {
        let text = `${item.name}: `
        if (filter.min !== undefined) text += `min ${filter.min}`
        if (filter.min !== undefined && filter.max !== undefined) text += ' - '
        if (filter.max !== undefined) text += `max ${filter.max}`
        return text
      }

      return `${item.name}: ${filter.value}`
    },

    addFilter() {
      if (!this.selectedItem || !this.canAddFilter) return

      const filterToAdd = {
        item: this.selectedItem.id,
        itemType: this.selectedItem.item_type,
        itemName: this.selectedItem.name
      } as any

      if (this.isNumericType(this.selectedItem.item_type)) {
        if (this.newFilter.min !== null) filterToAdd.min = this.newFilter.min
        if (this.newFilter.max !== null) filterToAdd.max = this.newFilter.max
      } else {
        filterToAdd.value = this.newFilter.value
      }

      this.addedFilters.push(filterToAdd)

      this.newFilter = {
        item: null,
        value: null,
        min: null,
        max: null
      }
    },

    removeAddedFilter(index: number) {
      this.addedFilters.splice(index, 1)
    },

    applyFilters() {
      const queryParams: Record<string, string> = {}

      this.addedFilters.forEach(filter => {
        if (this.isNumericType(filter.itemType)) {
          if (filter.min !== undefined) {
            queryParams[`${filter.itemName}_min`] = filter.min.toString()
          }
          if (filter.max !== undefined) {
            queryParams[`${filter.itemName}_max`] = filter.max.toString()
          }
        } else {
          queryParams[filter.itemName] = filter.value
        }
      })

      const labelFilterValue = this.labelFilter
      const labelFilterName = typeof this.labelFilter === 'number' 
        ? this.labels.find(l => l.id === this.labelFilter)?.text
        : this.labelFilter

      this.$emit('apply-filters', {
        status: this.statusFilter,
        filters: [
          ...this.addedFilters.map(f => ({ 
            ...f, 
            type: 'perspective' 
          })),
          ...(this.labelFilter !== null ? [{ 
            type: 'label',
            value: labelFilterValue,
            labelName: labelFilterName
          }] : [])
        ],
        filterMode: this.filterMode,
        queryParams
      })

      this.$emit('cancel')
    },

    resetFilters() {
      this.statusFilter = 'all'
      this.filterMode = 'every'
      this.labelFilter = null
      this.addedFilters = []
      this.newFilter = {
        item: null,
        value: null,
        min: null,
        max: null
      }
    }
  }
})
</script>

<style>
.v-divider {
	margin-bottom: 16px;
}
</style>