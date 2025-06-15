<template>
    <div>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="footerProps"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <!-- Search Field (unchanged) -->
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

    <!-- Items Column (unchanged) -->
    <template #[`item.items`]="{ item }">
      <div>
        <template v-for="(id, index) in visibleItems(item)">
          <v-chip
            v-if="index < 9"
            :key="id"
            color="primary"
            small
            class="ma-1"
            @click.stop="openItemDetails(id)"
          >
            {{ getItemName(id) }}
          </v-chip>
        </template>

        <v-btn
          v-if="item.items.length > 9"
          text
          small
          class="ml-1"
          @click.stop="openItemDialog(item)"
        >
          +{{ item.items.length - 9 }} more
        </v-btn>
      </div>
    </template>

  </v-data-table>

  <!-- Enhanced Items Dialog -->
<v-dialog v-model="dialog" max-width="600px">
  <v-card class="rounded-lg">
    <v-card-title class="primary white--text pa-4">
      <span class="headline">Perspective Items</span>
      <v-spacer />
      <v-btn icon dark @click="dialog = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    
    <v-divider />
    
    <v-card-text class="pa-4">
      <div class="d-flex flex-wrap">
        <v-chip
          v-for="(item, index) in selectedItemIds"
          :key="index"
          class="ma-2"
          color="primary"
          @click.stop="openItemDetails(item)"
        >
          {{ getItemName(item) }}
        </v-chip>
      </div>
    </v-card-text>
    
    <v-card-actions class="pa-4">
      <v-spacer />
      <v-btn
        color="primary"
        text
        @click="dialog = false"
      >
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
  <!-- Enhanced Item Details Dialog -->
  <v-dialog
    v-model="itemDetailDialog"
    max-width="600px"
    @keydown.esc="itemDetailDialog = false"
  >
    <v-card v-if="detailedItem" :loading="detailLoading" class="rounded-lg">
      <v-card-title class="primary white--text pa-4">
        <span class="headline">Item Details</span>
        <v-spacer />
        <v-btn icon dark @click="itemDetailDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-divider />
      
      <v-card-text class="pa-4">
        <v-simple-table>
          <tbody>
            <tr>
              <td class="font-weight-bold primary--text text--lighten-2">Name</td>
              <td>{{ detailedItem.name }}</td>
            </tr>
            <tr>
              <td class="font-weight-bold primary--text text--lighten-2">Type</td>
              <td>{{ detailedItem.item_type }}</td>
            </tr>
            <tr v-if="detailedItem.selection_list && detailedItem.item_type == 'list'">
              <td class="font-weight-bold primary--text text--lighten-2">Selection List</td>
              <td>
                <div class="d-flex flex-wrap">
                  <v-chip
                    v-for="(value, index) in detailedItem.selection_list"
                    :key="index"
                    class="ma-1"
                    color="secondary"
                    outlined
                    small
                  >
                    {{ value }}
                  </v-chip>
                </div>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-card-text>
      
      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn
          color="primary"
          text
          @click="itemDetailDialog = false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script lang="ts">
import { mdiMagnify, mdiClose, mdiTag } from '@mdi/js'
import Vue from 'vue'
import { Perspective } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<Perspective[]>,
      default: () => [],
      required: true
    },
    perspectiveItems: {
      type: Array,
      required: true
    },
    value: {
      type: Array as PropType<Perspective[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      search: '',
      mdiMagnify,
      mdiClose,
      mdiTag,
      dialog: false,
      itemDetailDialog: false,
      detailLoading: false,
      selectedItemIds: [] as (number | string)[],
      detailedItem: null as any,
      footerProps: {
        showFirstLastPage: true,
        'items-per-page-text': this.$t('vuetify.itemsPerPageText'),
        'page-text': this.$t('dataset.pageText')
      }
    }
  },

  computed: {
    headers() {
    return [
      { 
        text: 'Name', 
        value: 'name',
        width: '30%' // Explicit width
      },
      { 
        text: 'items', 
        value: 'items',
        width: '70%' // Explicit width
      },
    ]    }
  },

  methods: {
    visibleItems(item: Perspective) {
      return item.items || []
    },

    getItemName(id: number | string) {
      const found = this.perspectiveItems.find(i => i.id === id)
      return found ? found.name : 'Unknown'
    },

    openItemDialog(perspective: Perspective) {
      this.selectedItemIds = [...(perspective.items || [])]
      this.dialog = true
    },

    openItemDetails(id: number | string) {
      this.detailLoading = true
      this.dialog = false
      
      try {
        const item = this.perspectiveItems.find(i => i.id === id)
        if (item) {
          this.detailedItem = { ...item }
          this.itemDetailDialog = true
        }
      } finally {
        this.detailLoading = false
      }
    },

    formatDate(dateStr: string) {
      return new Date(dateStr).toLocaleString()
    }
  }
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

/* Add some subtle shadow to dialogs */
.v-card {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1) !important;
}

/* Better spacing for table rows */
.v-data-table >>> tbody tr {
  height: 52px;
}

/* Style for the primary header */
.primary--header {
  background-color: var(--v-primary-base);
  color: white;
}
</style>
