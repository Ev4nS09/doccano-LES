<template>
	<div>
	  <v-dialog v-model="confirmCloseDialog" max-width="400">
		<v-card>
		  <v-card-title>Confirm Close Ticket</v-card-title>
		  <v-card-text>Are you sure you want to close this ticket?</v-card-text>
		  <v-card-actions>
			<v-spacer></v-spacer>
			<v-btn text @click="confirmCloseDialog = false">Cancel</v-btn>
			<v-btn color="primary" text @click="confirmCloseTicket">Confirm</v-btn>
		  </v-card-actions>
		</v-card>
	  </v-dialog>
  
	  <v-data-table
		:value="selectedTickets"
		:items="filteredTickets"
		:headers="headers"
		:loading="loading"
		:search="search"
		class="elevation-1"
		:footer-props="{
		  showFirstLastPage: true,
		  'items-per-page-text': $t('vuetify.itemsPerPageText'),
		  'page-text': $t('dataset.pageText')
		}"
		show-select
		@input="$emit('update:selectedTickets', $event)"
	  >
		<template #top>
		  <v-text-field
			v-model="search"
			:prepend-inner-icon="mdiMagnify"
			:label="$t('generic.search')"
			single-line
			hide-details
			filled
			class="px-4"
		  />
		</template>
  
		<template #[`item.status`]="{ item }">
		  <v-chip :color="getStatusColor(item.status)" small>
			{{ item.status }}
		  </v-chip>
		</template>
  
		<template #[`item.created_at`]="{ item }">
		  {{ formatDate(item.created_at) }}
		</template>
  
		<template #[`item.author_username`]="{ item }">
		  <span>{{ item.author_name || item.author_username 
		  || (item.created_by === currentUserId ? 'You' : 'Unknown') }}</span>
		</template>
  
		<template #[`item.rules`]="{ item }">
		  <v-chip
			v-for="rule in getTicketRules(item)"
			:key="rule.id"
			small
			class="mr-1 mb-1"
		  >
			{{ rule.title }}
		  </v-chip>
		</template>
  
		<template #[`item.actions`]="{ item }">
		  <v-btn icon @click="$emit('open-chat', item)">
			<v-icon>{{ mdiMessageText }}</v-icon>
		  </v-btn>
		  <v-btn 
			v-if="item.status === 'open' && (isProjectAdmin || item.created_by === currentUserId)"
			icon 
			@click="openCloseDialog(item)" 
		  >
			<v-icon>{{ mdiLock }}</v-icon>
		  </v-btn>
		</template>
	  </v-data-table>
	</div>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { mdiMessageText, mdiLock, mdiMagnify } from '@mdi/js'
  import { TicketDTO } from '~/services/application/tickets/ticketData'
  import { RuleDTO } from '~/services/application/rule/ruleData'
  
  export default Vue.extend({
	props: {
	  tickets: {
		type: Array as () => TicketDTO[],
		required: true
	  },
	  rules: {
		type: Array as () => RuleDTO[],
		required: true
	  },
	  loading: {
		type: Boolean,
		default: false
	  },
	  selectedTickets: {
		type: Array as () => TicketDTO[],
		default: () => []
	  },
	  isProjectAdmin: {
		type: Boolean,
		default: false
	  },
	  currentUserId: {
		type: Number,
		default: null
	  },
	  statusFilter: {
		type: String,
		default: 'open'
	  }
	},
  
	data() {
	  return {
		mdiMessageText,
		mdiLock,
		mdiMagnify,
		search: '',
		confirmCloseDialog: false,
		ticketToClose: null as TicketDTO | null,
		headers: [
		  { 
			text: 'Title', 
			value: 'title',
			width: '200px'
		  },
		  { 
			text: 'Status', 
			value: 'status',
			width: '120px'
		  },
		  { 
			text: 'Created At', 
			value: 'created_at',
			width: '180px'
		  },
		  { 
			text: 'Created By', 
			value: 'author_username',
			width: '150px'
		  },
		  { 
			text: 'Related Rules', 
			value: 'rules',
			width: '250px'
		  },
		  { 
			text: 'Actions', 
			value: 'actions', 
			sortable: false,
			width: '120px'
		  }
		]
	  }
	},
  
	computed: {
	  filteredTickets() {
		return this.tickets.filter(t => t.status === this.statusFilter)
	  }
	},
  
	methods: {
	  getStatusColor(status: string) {
		switch (status) {
		  case 'open': return 'green'
		  case 'closed': return 'red'
		  case 'resolved': return 'blue'
		  default: return 'grey'
		}
	  },
  
	  formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('pt-PT', {
		  year: 'numeric',
		  month: '2-digit',
		  day: '2-digit',
		  hour: '2-digit',
		  minute: '2-digit'
		})
	  },
  
	  getTicketRules(ticket: TicketDTO) {
		if (!ticket.rules || !this.rules) return []
		return this.rules.filter(rule => ticket.rules.includes(rule.id))
	  },
  
	  openCloseDialog(ticket: TicketDTO) {
		this.ticketToClose = ticket
		this.confirmCloseDialog = true
	  },
  
	  confirmCloseTicket() {
		if (this.ticketToClose) {
		  this.$emit('close-ticket', this.ticketToClose)
		  this.confirmCloseDialog = false
		  this.ticketToClose = null
		}
	  }
	}
  })
  </script>
  
  <style scoped>
  ::v-deep .v-data-table td {
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
  }
  </style>