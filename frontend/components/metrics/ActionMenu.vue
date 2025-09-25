<template>
	<v-menu>
		<template #activator="{ on, attrs }">
			<v-btn color="primary text-capitalize" v-bind="attrs" v-on="on" :loading="exporting">
				<v-icon left>{{ mdiDownload }}</v-icon>
				Export
			</v-btn>
		</template>
		<v-list>
			<v-list-item @click="$emit('export', 'csv')">
				<v-list-item-title>CSV</v-list-item-title>
			</v-list-item>
			<v-list-item @click="$emit('export', 'json')">
				<v-list-item-title>JSON</v-list-item-title>
			</v-list-item>
			<v-list-item @click="$emit('export', 'pdf')">
				<v-list-item-title>PDF</v-list-item-title>
			</v-list-item>
		</v-list>
	</v-menu>
</template>

<script>
import { mdiDownload } from '@mdi/js'

export default {
	props: {
		exporting: Boolean
	},
	data() {
		return {
			mdiDownload
		}
	}
}
</script>