<template>
	<v-card>
	  <v-card-title>
		Manage Lock Status
	  </v-card-title>
	  <v-card-text>
		You are about to change the lock status of {{ selected.length }} item(s).
	  </v-card-text>
	  <v-card-actions>
		<v-spacer />
		<v-btn text @click="$emit('cancel')">
		  {{ $t('generic.cancel') }}
		</v-btn>
		<v-btn outlined color="warning" text @click="$emit('block', true)">
		  Lock
		</v-btn>
		<v-btn outlined color="primary" text @click="$emit('block', false)">
		  Unlock
		</v-btn>
	  </v-card-actions>
	</v-card>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import { ExampleDTO } from '~/services/application/example/exampleData'
  
  export default Vue.extend({
	props: {
	  selected: {
		type: Array as () => ExampleDTO[],
		required: true
	  }
	}
  })
  </script>