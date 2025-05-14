<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
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
		  :label="$t('generic.search')"
		  single-line
		  hide-details
		  filled
		/>
	  </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import { dateFormat } from '@vuejs-community/vue-filter-date-format'
import { dateParse } from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<PerspectiveItem[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<PerspectiveItem[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      search: '',
      options: {} as DataOptions,
      mdiMagnify,
      dateFormat,
      dateParse
    }
  },

  computed: {
    headers(): { text: any; value: string; sortable?: boolean }[] {
      return [
        { text: 'Name', value: 'name' },
        { text: 'Type', value: 'p_type'},
        { text: 'Created At', value: 'created_at' },
        { text: 'Updated At', value: 'updated_at' },
      ]
    }
  },

  watch: {
    options: {
      handler() {
        this.updateQuery({
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: ((this.options.page - 1) * this.options.itemsPerPage).toString(),
q: this.search
          }
        })
      },
      deep: true
    },
  },

  methods: {
    updateQuery(payload: any) {
      const { sortBy, sortDesc } = this.options
      if (sortBy.length === 1 && sortDesc.length === 1) {
        payload.query.sortBy = sortBy[0]
        payload.query.sortDesc = sortDesc[0]
      } else {
        payload.query.sortBy = 'createdAt'
        payload.query.sortDesc = true
      }
      this.$emit('update:query', payload)
    }
  }
})
</script>

