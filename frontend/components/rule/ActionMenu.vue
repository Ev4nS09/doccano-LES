<template>
	<action-menu
	  :items="items"
	  text='Actions'
	  @create="$emit('create')"
	/>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { mdiPencil } from '@mdi/js'
  import ActionMenu from '~/components/utils/ActionMenu.vue'
  
  export default Vue.extend({
	components: {
	  ActionMenu
	},
  
	data() {
	  return {
		mdiPencil
	  }
	},
  
	computed: {
	  items() {
		return [
		  {
			title: 'Create Rule',
			icon: mdiPencil,
			event: 'create'
		  }
		]
	  }
	}
  })
  </script>