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
  
	 <template #[`item.title`]="{ item }">
		<div class="text-truncate" style="max-width: 100px">
		 {{ item.title }}
		</div>
	 </template>
	 
	 <template #[`item.description`]="{ item }">
		<div class="description-content">
		 {{ item.description }}
		</div>
	 </template>
	 
     <template #[`item.actions`]="{ item }">
		<v-tooltip bottom>
		  <template #activator="{ on, attrs }">
			<v-btn
			  icon
			  small
			  v-bind="attrs"
			  v-on="on"
			  @click.stop="$emit('votes', item)"
			  class="ml-2"
			>
			  <v-icon small>
				{{ mdiListStatus }}
			  </v-icon>
			</v-btn>
		  </template>
		  <span>Votes</span>
		</v-tooltip>

	  </template> 

          <template #[`item.status`]="{ item }">
    <div class="status-content">
      {{ getStatusText(item) }}
    </div>
  </template>
    </v-data-table>
  </template>
  
  <script lang="ts">
  import { 
	mdiMagnify, 
    mdiListStatus, 
	mdiInformation,
	mdiArrowUp,
	mdiArrowDown
  } from '@mdi/js'
  import type { PropType } from 'vue'
  import Vue from 'vue'
  import { RuleDTO } from '~/services/application/rule/ruleData'
  
  export default Vue.extend({
	props: {
	 isLoading: {
		type: Boolean,
		default: false,
		required: true
	 },
	 items: {
		type: Array as PropType<RuleDTO[]>,
		default: () => [],
		required: true
	 },
	 value: {
		type: Array as PropType<RuleDTO[]>,
		default: () => [],
		required: true
	 }
	},
  
	data() {
	 return {
		search: '',
		mdiMagnify,
		mdiInformation,
		mdiArrowUp,
        mdiListStatus,
		mdiArrowDown
	 }
	},

    methods: {
        getStatusText(item :RuleDTO)
        {
            const now = new Date()
            const start = new Date(item.start_at)
                
            return start > now ? 'Yet to Start' : item.status
        }
    },

	computed: {
	 headers() {
		return [
		 { 
			text: 'Title', 
			value: 'title', 
			sortable: true,
			width: '100px'
		 },
		 { 
			text: 'Description', 
			value: 'description', 
			sortable: true,
			width: '500px'
		 },
		 { 
			text: 'Actions', 
			value: 'actions', 
			sortable: false,
			width: '300px'
		 },
         {
            text: 'Voting Status',
            value: 'status',
            sortable: true,
            width: '150px'
          }
		]
	 }
	}
  })
  </script>
  
  <style scoped>
  .description-content {
	padding-left: 16px;
	white-space: normal;
	word-break: break-word;
	max-width: 800px;
	line-height: 1.5;
	padding-top: 12px !important;
	padding-bottom: 12px !important;
  }
  
  ::v-deep .v-data-table td {
	vertical-align: middle;
  }
  
  ::v-deep .v-data-table td:nth-child(2) {
	padding: 0 !important;
  }
  </style>%       
