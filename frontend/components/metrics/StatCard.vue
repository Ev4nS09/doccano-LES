<template>
	<v-tooltip bottom>
	  <template #activator="{ on, attrs }">
		<v-card class="stat-card" v-bind="attrs" v-on="on">
		  <v-card-text :class="['text-center', theme]">
			<v-icon x-large class="icon">{{ icon }}</v-icon>
			<div class="text-h5 font-weight-bold mt-2">{{ value }}</div>
			<div class="text-subtitle-1">{{ title }}</div>
		  </v-card-text>
		</v-card>
	  </template>
	  <span>{{ tooltip }}</span>
	</v-tooltip>
  </template>
  
  <script>
  import { computed, useContext } from '@nuxtjs/composition-api'
  
  export default {
	props: {
	  title: String,
	  value: [String, Number],
	  icon: String,
	  tooltip: String, // ← New prop
	},
	setup() {
	  const { $vuetify } = useContext();
	  const theme = computed(() => ($vuetify.theme.dark ? 'dark' : 'light'));
	  return {
		theme,
	  };
	}
  }
  </script>
  
  <style scoped>
  .text-center.light {
	background-color: #e0e0e038;
}

.text-center.dark {
	background-color: #252525;
}
  
  /* Icon color */
  .text-center.light .icon {
	color: #1976D2; /* Icon color for light theme */
  }
  
  .text-center.dark .icon {
	color: #21CFF3; /* Icon color for dark theme */
  }
  
  /* Text color matches the icon color */
  .text-center.light .text-h5,
  .text-center.light .text-subtitle-1 {
	color: black; /* Text color for light theme */
  }
  
  .text-center.dark .text-h5,
  .text-center.dark .text-subtitle-1 {
	color: white; /* Text color for dark theme */
  }
  </style>
  