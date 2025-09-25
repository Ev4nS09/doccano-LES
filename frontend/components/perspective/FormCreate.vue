<template>
  <base-card
    :disabled="!valid"
    :title="$t('Perspective')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="validateAndSave"
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

              <v-col cols="12" class="mt-4">
                <v-expansion-panels flat>
                  <v-expansion-panel>
                    <v-expansion-panel-header class="primary--text">
                      <template v-slot:default="{ open }">
                        <v-row no-gutters align="center">
                          <v-icon left color="primary">
                            {{ mdiPlus }}
                          </v-icon>
                          <span class="font-weight-medium">Create New Item</span>
                          <v-spacer />
                          <span v-if="!open && newItem.name" class="text-caption text--secondary">
                            {{ newItem.name }}
                          </span>
                        </v-row>
                      </template>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-form v-model="itemFormValid" ref="itemForm" class="px-2">
                        <v-text-field
                          v-model="newItem.name"
                          label="Item name"
                          placeholder="Enter item name"
                          outlined
                          dense
                          color="primary"
                          :rules="[rules.nameRequired, rules.nameSize]"
                          class="mb-3"
                        />

                        <v-autocomplete
                          v-model="newItem.item_type"
                          :items="types"
                          label="Item Type"
                          placeholder="Select a type"
                          outlined
                          dense
                          color="primary"
                          :rules="[rules.typeRequired]"
                          class="mb-3"
                        />

                        <v-combobox
                          v-if="newItem.item_type === 'list'"
                          v-model="newItem.selection_list"
                          label="List options"
                          multiple
                          chips
                          outlined
                          dense
                          color="primary"
                          placeholder="Add options"
                          class="mb-4"
                          deletable-chips
                          clearable
                        >
                          <template v-slot:selection="{ attrs, item, select, selected }">
                            <v-chip
                              v-bind="attrs"
                              :input-value="selected"
                              close
                              @click="select"
                              @click:close="removeOption(item)"
                              small
                              class="ma-1"
                            >
                              {{ item }}
                            </v-chip>
                          </template>
                        </v-combobox>
                        <v-btn
                          color="primary"
                          block
                          :disabled="!itemFormValid"
                          @click="createItem"
                          class="mt-2"
                        >
                          <v-icon left small>{{ mdiCheck }}</v-icon>
                          Add Item
                        </v-btn>
                      </v-form>

                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <!-- Duplicate name error -->
        <v-alert 
          v-if="duplicateError"
          dismissable 
          prominent
          type="error"
          class="mt-4"
                      @click:close="duplicateError = false"
        >
          A perspective with this name already exists
        </v-alert>

        <v-alert v-show="localErrorMessage" dismissable type="error"   
                    @click:close="localErrorMessage = ''">
          {{ localErrorMessage }}
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
              <v-icon>{{ mdiClose }}</v-icon>
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
import { 
  mdiCreditCardOutline, 
  mdiPlaylistCheck, 
  mdiInformation, 
  mdiClose,
  mdiPlus,
  mdiLabel,
  mdiFormatListBulletedType,
  mdiPlaylistEdit,
  mdiCheck
} from '@mdi/js'
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
  },

  data() {
    return {
      isLoading: false,
      valid: false,
      itemFormValid: false,
      perspectiveItems: [] as PerspectiveItem[],
      name: '',
      duplicateError: false,
      mdiPlaylistCheck,
      mdiCreditCardOutline,
      mdiInformation,
      mdiClose,
      mdiPlus,
      mdiLabel,
      mdiFormatListBulletedType,
      mdiPlaylistEdit,
      mdiCheck,
      selectedItems: [] as (string | number)[],
      itemDetailDialog: false,
      detailedItem: null as PerspectiveItem | null,
      newItem: {
        name: '',
        item_type: '',
        selection_list: [] as string[]
      },
      types: ['int', 'float', 'bool', 'list'],
      rules: {
        nameRequired: (v: string) => (!!v) || 'Name Required',
        nameSize: (v: string) => (!!(v.length < 101)) || 'Name must be less than 101 characters',
        typeRequired: (v: string) => (!!v) || 'Type Required',
        itemRequired: (v: (string | number)[]) => (!!v.length) || 'At least one item required'
      },
      localErrorMessage: '' as string,
      itemDuplicateError: false, // Add this line
    }
  },

  methods: {
    async validateAndSave() {
      try {
        this.duplicateError = false;
        const perspectives = await this.$repositories.perspective.listPerspective();
        const nameExists = perspectives.some(p => 
          p.name.toLowerCase() === this.name.toLowerCase()
        );

        if (nameExists) {
          this.duplicateError = true;
          return;
        }

        this.$emit('save', { name: this.name, perspectiveItems: this.selectedItems });
      } catch (error) {
        console.error('Error validating perspective:', error);
        this.duplicateError = true;
      }
    },

    openItemDetails(item: PerspectiveItem, event?: Event) {
      event?.stopPropagation();
      this.detailedItem = item;
      this.itemDetailDialog = true;
    },

    closeItemDetails() {
      this.itemDetailDialog = false;
      this.$nextTick(() => {
        const input = (this.$refs.autocomplete as any).$refs.input;
        if (input) {
          input.focus();
        }
      });
    },

    removeOption(item: string) {
      this.newItem.selection_list = this.newItem.selection_list.filter(
        (option) => option !== item
      );
    },

async createItem() {
  try {
    this.itemDuplicateError = false; // Reset error state
    this.localErrorMessage = ''; // Clear any previous errors

    // Check for duplicate name in perspectiveItems (local list)
    const nameExists = this.perspectiveItems.some(item => 
      item.name.toLowerCase() === this.newItem.name.toLowerCase()
    );

    if (nameExists) {
      this.itemDuplicateError = true;
      this.localErrorMessage = 'An item with this name already exists';
      return;
    }

    const itemData = {
      name: this.newItem.name,
      item_type: this.newItem.item_type,
      selection_list: this.newItem.item_type === 'list' ? this.newItem.selection_list : []
    };

    const newItem = { 
      id: -1, 
      ...itemData,
      createdAt: '', 
      updatedAt: ''
    } as PerspectiveItem;
    
    const createdItem = await this.$repositories.perspective.createPerspectiveItem(newItem);
    this.perspectiveItems.push(createdItem);
    this.selectedItems.push(createdItem.id);
    
    this.newItem = {
      name: '',
      item_type: '',
      selection_list: []
    };
    (this.$refs.itemForm as any).resetValidation();
    this.localErrorMessage = '';
    
  } catch (error) {
    console.error('Error creating item:', error);
    this.localErrorMessage = 'Failed to create item';
  }
}  },

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
