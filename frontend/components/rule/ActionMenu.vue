<template>
	<action-menu
	  :items="items"
	  text="Actions"
        @create-rule="$emit('create-rule')"	  
        @create-ticket="$emit('create-ticket')"
	/>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { mdiPencil, mdiTicket } from '@mdi/js'
  import ActionMenu from '~/components/utils/ActionMenu.vue'
  
  export default Vue.extend({
	components: {
	  ActionMenu
	},
  
	props: {
	  isProjectAdmin: {
		type: Boolean,
		default: false
	  }
	},
  
	data() {
	  return {
		mdiPencil,
		mdiTicket
	  }
	},
  
	computed: {
	  items() {
		const actions = [
		  {
			title: 'Create Ticket',
			icon: this.mdiTicket,
			event: 'create-ticket'
		  }
		]
  
		if (this.isProjectAdmin) {
		  actions.unshift({
			title: 'Create Rule',
			icon: this.mdiPencil,
			event: 'create-rule'
		  })
		}
  
		return actions
	  }
	}
  })
  </script>
  
