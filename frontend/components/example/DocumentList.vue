<template>
  <div>
    <v-data-table
      :value="value"
      :headers="headers"
      :items="items"
      :options.sync="options"
      :server-items-length="total"
      :search="search"
      :loading="isLoading"
      :loading-text="$t('generic.loading')"
      :no-data-text="$t('vuetify.noDataAvailable')"
      :footer-props="{
        showFirstLastPage: true,
        'items-per-page-options': [10, 50, 100],
        'items-per-page-text': $t('vuetify.itemsPerPageText'),
        'page-text': $t('dataset.pageText')
      }"
      item-key="id"
      show-select
      @input="$emit('input', $event)"
    >
      <template #top>
        <v-text-field
          v-model="search"
          :prepend-inner-icon="mdiMagnify"
          :label="$t('generic.search') + ' (e.g. label:positive)'"
          single-line
          hide-details
          filled
        />
      </template>
      <template #[`item.status`]="{ item }">
        <v-chip v-if="item.blocked" color="error" small>
          Locked
        </v-chip>
        <v-chip v-else :color="item.isConfirmed ? 'success' : 'warning'" small>
          {{ item.isConfirmed ? 'Finished' : 'In progress' }}
        </v-chip>
      </template>
      <template #[`item.text`]="{ item }">
        <span class="d-flex d-sm-none">{{ item.text | truncate(50) }}</span>
        <span class="d-none d-sm-flex">{{ item.text | truncate(200) }}</span>
      </template>
      <template #[`item.meta`]="{ item }">
        {{ JSON.stringify(item.meta, null, 4) }}
      </template>
      <template #[`item.agreement`]="{ item }">
        <div style="display: flex; gap: 8px; justify-content: left;">
          <!-- Label Agreement Ball -->
          <v-tooltip bottom>
            <template #activator="{ on }">
              <svg width="24" height="24" viewBox="0 0 16 16" v-on="on">
                <circle cx="8" cy="8" r="6" :fill="getLabelAgreementColor(item)" />
              </svg>
            </template>
          </v-tooltip>
            <div>
              {{ getAgreementLabel(item) }}
            </div>
        </div>
      </template>
      <template #[`item.assignee`]="{ item }">
        <v-combobox
          :value="toSelected(item)"
          :items="members"
          item-text="username"
          no-data-text="No one"
          multiple
          chips
          dense
          flat
          hide-selected
          hide-details
          small-chips
          solo
          style="width: 200px"
          @change="onAssignOrUnassign(item, $event)"
        >
          <template #selection="{ attrs, item, parent, selected }">
            <v-chip v-bind="attrs" :input-value="selected" small class="mt-1 mb-1">
              <span class="pr-1">{{ item.username }}</span>
              <v-icon small @click="parent.selectItem(item)"> $delete </v-icon>
            </v-chip>
          </template>
        </v-combobox>
      </template>
      <template #[`item.action`]="{ item }">
        <template v-if="!item.blocked">
          <v-btn class="me-1" small color="primary text-capitalize" @click="$emit('edit', item)">
            Edit
          </v-btn>
          <v-btn small color="primary text-capitalize" @click="toLabeling(item)">
            {{ $t('dataset.annotate') }}
          </v-btn>
        </template>
        <template v-else>
          <v-btn 
            small 
            color="primary text-capitalize" 
            @click.stop="showStatsOverlay(item)"
          >
            Stats
          </v-btn>
          <v-btn small color="primary text-capitalize" @click="$emit('discrepancies', item)">
            {{ $t('Discrepancies') }}
          </v-btn>
        </template>
      </template>
    </v-data-table>
    <v-dialog 
      v-model="showMemberStats" 
      max-width="800px"
      scrollable
      persistent
    >
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span></span>
          <v-btn icon @click="showMemberStats = false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,
              17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
            </svg>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <Statistics
            v-if="selectedExample"
            :project-id="projectId"
            :example-id="selectedExample.id"
            :teacher-list="members"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { mapGetters } from 'vuex';
import { DataOptions } from 'vuetify/types'
import { ExampleDTO } from '~/services/application/example/exampleData'
import { MemberItem } from '~/domain/models/member/member'
import { APIMemberRepository } from '~/repositories/member/apiMemberRepository'
import Statistics from '~/components/example/Statistics.vue'
import { APILabelRepository } from '~/repositories/label/apiLabelRepository'
import { LabelDTO } from '~/services/application/label/labelData';


export default Vue.extend({
  components: {
    Statistics
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    },
    members: {
      type: Array as PropType<MemberItem[]>,
      default: () => [],
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    },
    projectId: {
      type: [String, Number],
      required: true
    },
    exampleId: {
      type: [String, Number],
      required: false
    },
    memberStats: {
      type: Object as PropType<Record<string, { percentage: number, topLabel?: number }>>,
      default: () => ({}),
      required: false
    },
    labels: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: false
    }
  },

  data() {
    return {
      search: this.$route.query.q,
      options: {} as DataOptions,
      mdiMagnify,
      agreementPercentage: 0,
      isLoadingStats: false,
      statsError: null as string | null,
      memberRepository: new APIMemberRepository(),
      showMemberStats: false,
      selectedExample: null as ExampleDTO | null,
      isLoadingOverlay: false,
      labelRepository: new APILabelRepository(),
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    headers() {
      const headers = [
        {
          text: 'Status',
          value: 'status',
          sortable: false,
          width: '120px'
        },
        {
          text: this.$t('dataset.text'),
          value: 'text',
          sortable: false
        },
        {
          text: this.$t('dataset.metadata'),
          value: 'meta',
          sortable: false
        },
        {
          text: 'Agreement',
          value: 'agreement',
          sortable: false,
          width: '300px'
        },
        {
          text: this.$t('dataset.action'),
          value: 'action',
          sortable: false
        }
      ]
      if (this.isAdmin) {
        headers.splice(4, 0, {
          text: 'Assignee',
          value: 'assignee',
          sortable: false
        })
      }
      return headers
    }
  },

  watch: {
    options: {
      handler() {
        this.$emit('update:query', {
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: ((this.options.page - 1) * this.options.itemsPerPage).toString(),
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.$emit('update:query', {
        query: {
          limit: this.options.itemsPerPage.toString(),
          offset: '0',
          q: this.search
        }
      })
      this.options.page = 1
    }
  },

  methods: {
    getLabelName(labelId: number | undefined): string {
      if (!labelId) return '';
      const label = this.labels.find(l => l.id === labelId);
      return label?.text || '';
    },
    showStatsOverlay(item: ExampleDTO) {
      console.log('Showing stats for example:', item.id)
      this.selectedExample = item
      this.showMemberStats = true
      
      this.isLoadingOverlay = true
      setTimeout(() => {
        this.isLoadingOverlay = false
      }, 300)
    },

    getLabelAgreementColor(item: ExampleDTO) {
      if (this.isLoadingStats) return 'grey'
      if (this.statsError) return 'grey'
      if (!this.memberStats[item.id]) return 'grey'

      if (!item.blocked) return 'yellow'

      const { topLabel } = this.memberStats[item.id]
      if (topLabel === undefined) return 'red'
      
      return 'green'
    },

    toLabeling(item: ExampleDTO) {
      if (item.blocked) {
        return []
      }
      const index = this.items.indexOf(item)
      const offset = (this.options.page - 1) * this.options.itemsPerPage
      const page = (offset + index + 1).toString()
      this.$emit('click:labeling', { page, q: this.search })
    },

    toSelected(item: ExampleDTO) {
      const assigneeIds = item.assignments.map((assignment) => assignment.assignee_id)
      return this.members.filter((member) => assigneeIds.includes(member.user))
    },

    onAssignOrUnassign(item: ExampleDTO, newAssignees: MemberItem[]) {
      const newAssigneeIds = newAssignees.map((assignee) => assignee.user)
      const oldAssigneeIds = item.assignments.map((assignment) => assignment.assignee_id)
      if (oldAssigneeIds.length > newAssigneeIds.length) {
        for (const assignment of item.assignments) {
          if (!newAssigneeIds.includes(assignment.assignee_id)) {
            this.$emit('unassign', assignment.id)
          }
        }
      } else {
        for (const newAssigneeId of newAssigneeIds) {
          if (!oldAssigneeIds.includes(newAssigneeId)) {
            this.$emit('assign', item.id, newAssigneeId)
          }
        }
      }
    },

    publicGetLabelAgreementStatus(item: ExampleDTO) {
      if (!item.blocked) return 'discussion';
      if (this.memberStats[item.id]?.topLabel === undefined) return 'disagreement';
      return 'agreement';
    },

    getAgreementLabel(item: ExampleDTO): string {
      if (this.isLoadingStats) return 'Loading label agreement data...'
      if (this.statsError) return this.statsError
      if (!item.blocked) return 'In discussion'

      const stat = this.memberStats[item.id]
      if (!stat?.topLabel) return 'Label: Disagreement'

      const labelName = this.getLabelName(stat.topLabel)
      return `Label: ${labelName}`
    }
  }
})
</script>