<template>
	<v-card>
	  <v-card-title class="primary white--text">
		{{ rule.title }}
		<v-spacer />
		<v-btn icon dark @click="$emit('close')">
		  <v-icon>mdi-close</v-icon>
		</v-btn>
	  </v-card-title>
	  
	  <v-card-text class="pa-6">
		<v-row>
		  <!-- Left Column - Description -->
		  <v-col cols="12" md="8" class="d-flex flex-column">
			<div class="text-h6 mb-4">Description</div>
			<v-divider class="mb-4" />
			<div class="description-text flex-grow-1">
			  {{ rule.description }}
			</div>
		  </v-col>
		  
		  <!-- Right Column - Metadata -->
		  <v-col cols="12" md="4">
			<div class="metadata-container">
			  <div class="text-h6 mb-4">Details</div>
			  
			  <v-divider class="mb-4" />
			  
			  <div class="d-flex align-center mb-3">
				<v-icon left color="primary">mdi-account</v-icon>
				<div>
				  <div class="text-caption grey--text">Created by</div>
				  <div>{{ authorName }}</div>
				</div>
			  </div>
			  
			  <div class="d-flex align-center mb-3">
				<v-icon left color="primary">mdi-calendar</v-icon>
				<div>
				  <div class="text-caption grey--text">Created at</div>
				  <div>{{ formatDate(rule.created_at) }}</div>
				</div>
			  </div>
			  
			  <div class="d-flex align-center">
				<v-icon left color="primary">mdi-star</v-icon>
				<div>
				  <div class="text-caption grey--text">Score</div>
				  <div :class="scoreColorClass">{{ rule.score }}</div>
				</div>
			  </div>
			</div>
		  </v-col>
		</v-row>
	  </v-card-text>
	</v-card>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { RuleDTO } from '~/services/application/rule/ruleData'
  
  export default Vue.extend({
	props: {
	  rule: {
		type: Object as () => RuleDTO,
		required: true
	  },
	  projectId: {
		type: String,
		required: true
	  }
	},
  
	data() {
	  return {
		members: [] as any[],
		isLoadingMembers: false
	  }
	},
  
	computed: {
	  scoreColorClass(): string {
		if (this.rule.score > 0) return 'green--text'
		if (this.rule.score < 0) return 'red--text'
		return 'grey--text'
	  },
	  authorName(): string {
		// First try the direct author_username if available
		if (this.rule.author_username) {
		  return this.rule.author_username
		}
		
		// Then try to find in members list
		if (this.rule.created_by && this.members.length > 0) {
		  const member = this.members.find(m => m.user === this.rule.created_by)
		  if (member) {
			return member.username || `User ${this.rule.created_by}`
		  }
		}
		
		// Fallback
		return `User ${this.rule.created_by}`
	  }
	},
  
	async created() {
	  await this.fetchMembers()
	},
  
	methods: {
	  formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
		  year: 'numeric',
		  month: 'long',
		  day: 'numeric',
		  hour: '2-digit',
		  minute: '2-digit'
		})
	  },
	  
	  async fetchMembers() {
		try {
		  this.isLoadingMembers = true
		  this.members = await this.$repositories.member.list(this.projectId)
		} catch (e) {
		  console.error('Failed to fetch members', e)
		} finally {
		  this.isLoadingMembers = false
		}
	  }
	}
  })
  </script>
  
  <style scoped>
  .v-card-title {
	padding: 16px 24px;
  }
  
  .description-text {
	min-height: 120px;
	display: flex;
	flex-direction: column;
  }
  
  .metadata-container {
	padding-left: 16px;
  }
  
  /* Theme-specific styles */
  .theme--light .description-text {
	color: rgba(0, 0, 0, 0.87);
  }
  
  .theme--dark .description-text {
	color: rgba(255, 255, 255, 0.87);
  }
  </style>