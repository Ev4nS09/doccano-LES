<template>
  <base-card
    :disabled="!valid"
    :title="$t('Perspective')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('save', { name: name, perspectiveItems: selectedItems })"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-card-text>
          <v-form v-model="valid">
            <v-row dense>
              <v-col cols="12">
                <v-text-field
                  v-model="name"
                  label="Perspective name"
                  placeholder="Enter a perspective name"
                  outlined
                  dense
                  color="primary"
                  :rules="[rules.nameRequired, rules.nameSize]"
                  :prepend-icon="mdiCreditCardOutline"
                />
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="selectedItems"
                  :items="perspectiveItems"
                  item-text="name"
                  item-value="id"
                  label="Select Items"
                  multiple
                  chips
                  small-chips
                  deletable-chips
                  outlined
                  dense
                  color="primary"
                  hide-details="auto"
                  placeholder="Choose one or more"
                  :rules="[rules.itemRequired]"
                  :prepend-icon="mdiPlaylistCheck"
                  :menu-props="{ closeOnContentClick: false }"
                  ref="autocomplete"
                >
                  <template #item="{ item, on, attrs }">
                    <v-list-item v-bind="attrs" v-on="on">
                      <v-list-item-content>
                        <v-list-item-title>{{ item.name }}</v-list-item-title>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn
                          icon
                          small
                          @click.stop="openItemDetails(item, $event)"
                        >
                          <v-icon small>{{ mdiInformation }}</v-icon>
                        </v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-alert v-show="errorMessage" prominent type="error">
          <v-row align="center">
            <v-col class="grow">
              {{ errorMessage }}
            </v-col>
          </v-row>
        </v-alert>
      </v-form>

      <!-- Item Details Dialog -->
      <v-dialog
        v-model="itemDetailDialog"
        max-width="600px"
        @keydown.esc="itemDetailDialog = false"
      >
        <v-card v-if="detailedItem" class="rounded-lg">
          <v-card-title class="primary white--text pa-4">
            <span class="headline">Item Details</span>
            <v-spacer />
            <v-btn icon dark @click="closeItemDetails">
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
              @click="closeItemDetails"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </base-card>
</template>

<script lang="ts">
import { mdiCreditCardOutline, mdiPlaylistCheck, mdiInformation, mdiClose } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'
import { Perspective } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    value: {
      type: Object as PropType<Perspective>,
      required: true
    },
    errorMessage: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      isLoading: false,
      valid: false,
      perspectiveItems: [] as PerspectiveItem[],
      name: '',
      mdiPlaylistCheck,
      mdiCreditCardOutline,
      mdiInformation,
      mdiClose,
      selectedItems: [] as (string | number)[],
      itemDetailDialog: false,
      detailedItem: null as PerspectiveItem | null,
      rules: {
        nameRequired: (v: string) => (!!v) || 'Name Required',
        nameSize: (v: string) => (!!(v.length < 101)) || 'Name must be less than 101 characters',
        itemRequired: (v: (string | number)[]) => (!!v.length) || 'At least one item required'
      },
    }
  },

  methods: {
    openItemDetails(item: PerspectiveItem, event?: Event) {
      event?.stopPropagation();
      this.detailedItem = item;
      this.itemDetailDialog = true;
    },

    closeItemDetails() {
      this.itemDetailDialog = false;
      // Re-focus the autocomplete to keep the menu open
      this.$nextTick(() => {
        const input = (this.$refs.autocomplete as any).$refs.input;
        if (input) {
          input.focus();
        }
      });
    }
  },

  async fetch() {
    this.isLoading = true;
    this.perspectiveItems = await this.$repositories.perspective.listAllPerspectiveItem();
    this.isLoading = false;
  },

  watch: {
    name() {
      if (this.perspectiveItems.length > 0) return;
      if (this.isLoading) return;
      this.$fetch();
    }
  }
})
</script>

<style scoped>
.v-list-item__action {
  margin-left: 8px;
  min-width: 24px;
}
</style>
