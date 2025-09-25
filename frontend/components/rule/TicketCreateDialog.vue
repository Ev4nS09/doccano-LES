<template>
	<v-dialog :value="show" max-width="800" persistent @input="$emit('close')">
	  <v-card>
		<v-card-title>
		  Create New Ticket
		  <v-spacer />
		  <v-btn icon @click="$emit('close')">
			<v-icon>{{ mdiClose }}</v-icon>
		  </v-btn>
		</v-card-title>
		<v-card-text>
		  <v-text-field
			v-model="title"
			label="Ticket Title"
			outlined
			required
		  />
  
		  <v-select
			v-model="selectedRules"
			:items="rules"
			item-text="title"
			item-value="id"
			multiple
			return-object
			label="Related Rules"
			chips
			outlined
			required
		  />
  
		  <v-textarea
			v-model="description"
			label="Description"
			outlined
			required
		  />
		</v-card-text>
		<v-card-actions>
		  <v-spacer />
		  <v-btn @click="$emit('close')">Cancel</v-btn>
		  <v-btn 
			color="primary" 
			@click="handleCreate" 
			:loading="loading"
			:disabled="!title.trim() || !description.trim() || !selectedRules.length"
		  >
			Create
		  </v-btn>
		</v-card-actions>
	  </v-card>
	</v-dialog>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { mdiClose } from '@mdi/js'
  import { RuleDTO } from '~/services/application/rule/ruleData'
  
  export default Vue.extend({
	props: {
	  show: {
		type: Boolean,
		required: true
	  },
	  rules: {
		type: Array as () => RuleDTO[],
		required: true
	  },
	  loading: {
		type: Boolean,
		default: false
	  }
	},
  
	data() {
	  return {
		mdiClose,
		title: '',
		description: '',
		selectedRules: [] as RuleDTO[]
	  }
	},
  
	methods: {
	  resetForm() {
		this.title = ''
		this.description = ''
		this.selectedRules = []
	  },
  
	  handleCreate() {
		if (!this.title.trim() || !this.description.trim() || !this.selectedRules.length) return
  
		this.$emit('create', { 
		  title: this.title, 
		  description: this.description,
		  selectedRules: this.selectedRules
		})
		this.resetForm()
	  }
	},
  
	watch: {
	  show(newVal) {
		if (!newVal) {
		  this.resetForm()
		}
	  }
	}
  })
  </script>
  