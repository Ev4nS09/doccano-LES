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
	  
	  <!-- Title Column -->
	  <template #[`item.title`]="{ item }">
		<div class="text-truncate" style="max-width: 100px">
		  {{ item.title }}
		</div>
	  </template>
	  
	  <!-- Description Column with wrapping and padding -->
	  <template #[`item.description`]="{ item }">
		<div class="description-content">
		  {{ item.description }}
		</div>
	  </template>
	  
	  <template #[`item.score`]="{ item }">
		<div class="d-flex align-center">
		  <v-btn icon small @click.stop="$emit('downvote', item)">
			<v-icon small :color="item.user_vote === -1 ? 'primary' : ''">
			  {{ mdiArrowDown }}
			</v-icon>
		  </v-btn>
		  <v-btn icon small @click.stop="$emit('upvote', item)">
			<v-icon small :color="item.user_vote === 1 ? 'primary' : ''">
			  {{ mdiArrowUp }}
			</v-icon>
		  </v-btn>
		  
		  <div class="mx-1">
			{{ item.score }}
		  </div>
		</div>
	  </template>

	  <template #[`item.status`]="{ item }">
		<div class="text-truncate" style="max-width: 100px">
		  {{ item.status }}
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
			  @click.stop="$emit('details', item)"
			>
			  <v-icon small>
				{{ mdiInformation }}
			  </v-icon>
			</v-btn>
		  </template>
		  <span>Details</span>
		</v-tooltip>
		
		<v-tooltip bottom>
		  <template #activator="{ on, attrs }">
			<v-btn
			  icon
			  small
			  v-bind="attrs"
			  v-on="on"
			  @click.stop="$emit('chat', item)"
			  class="ml-2"
			>
			  <v-icon small>
				{{ mdiMessageText }}
			  </v-icon>
			</v-btn>
		  </template>
		  <span>Chat</span>
		</v-tooltip>

		<v-tooltip bottom>
		  <template #activator="{ on, attrs }">
			<v-btn
			  icon
			  small
			  v-bind="attrs"
			  v-on="on"
			  @click.stop="$emit('status', item)"
			  class="ml-2"
			>
			  <v-icon small>
				{{ mdiListStatus }}
			  </v-icon>
			</v-btn>
		  </template>
		  <span>Details</span>
		</v-tooltip>

	  </template>
	</v-data-table>
  </template>
  
  <script lang="ts">
  import { 
	mdiMagnify, 
	mdiInformation, 
	mdiMessageText,
    mdiListStatus,
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
        mdiListStatus,
		mdiMessageText,
		mdiArrowUp,
		mdiArrowDown
	  }
	},
  
	computed: {
	  headers() {
		return [
		  { 
			text: 'Title', 
			value: 'title', 
			sortable: true,
			width: '100px'  // Explicit width for column
		  },
		  { 
			text: 'Description', 
			value: 'description', 
			sortable: true,
			width: '500px'  // Explicit width for column
		  },
		  { 
			text: 'Score', 
			value: 'score', 
			sortable: true,
			width: '150px'  // Fixed width for score column
		  },
		  { 
			text: 'Actions', 
			value: 'actions', 
			sortable: false,
			width: '120px'  // Fixed width for actions
		  },
          {
            text: 'Status',
            value: 'status',
            sortable: true,
            width: '150px'
          }

		]
	  }
	},
  
	methods: {
	  getScoreColor(score: number): string {
		if (score > 0) return 'green'
		if (score < 0) return 'red'
		return 'grey'
	  }
	}
  })
  </script>
  
  <style scoped>
/* Description cell styling */
.description-content {
  padding-left: 16px;
  white-space: normal;
  word-break: break-word;
  max-width: 800px;
  line-height: 1.5;
  padding-top: 12px !important; /* Ensures top padding */
  padding-bottom: 12px !important; /* Ensures bottom padding */
}

/* Table cell alignment */
::v-deep .v-data-table td {
  vertical-align: middle;
}

/* Specific padding for description column */
::v-deep .v-data-table td:nth-child(2) {
  padding: 0 !important; /* Remove default cell padding */
}
  </style>
