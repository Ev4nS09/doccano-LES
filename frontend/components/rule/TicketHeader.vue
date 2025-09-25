<template>
	<v-card-title>
	  <!-- Always show the create ticket option via RuleActionMenu -->
	  <rule-action-menu 
		@create-rule="$emit('create-rule')" 
		@create-ticket="$emit('open-ticket-dialog')"
		:is-project-admin="isProjectAdmin"
	  />
  
	  <!-- Show Delete button only for admins -->
	  <v-btn
		v-if="isProjectAdmin"
		class="text-capitalize ms-2"
		:disabled="!canDelete"
		outlined
		@click.stop="$emit('open-delete-dialog')"
	  >
		{{ $t('generic.delete') }}
	  </v-btn>
	</v-card-title>
  </template>
  
  
  <script lang="ts">
  import Vue from 'vue'
  import RuleActionMenu from '~/components/rule/ActionMenu.vue'
  
  export default Vue.extend({
	components: {
	  RuleActionMenu
	},
  
	props: {
	  isProjectAdmin: {
		type: Boolean,
		required: true
	  },
	  canDelete: {
		type: Boolean,
		required: true
	  }
	}
  })
  </script>
