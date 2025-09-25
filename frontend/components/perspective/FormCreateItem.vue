<template>
  <base-card
    :disabled="!valid"
    :title="$t('Item')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="validateAndSave"
    @cancel="$emit('cancelItem')"
  >
    <template #content>
      <v-form v-model="valid">
        <v-card-text>
          <v-form v-model="valid">
            <v-row dense>
              <v-col cols="12">
                <v-text-field
                  v-model="name"
                  label="Item name"
                  placeholder="Enter a name"
                  outlined
                  dense
                  color="primary"
                  :rules="[rules.nameRequired, rules.nameSize]"
                  :prepend-icon="mdiCreditCardOutline"
                />
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="type"
                  :items="types"
                  :loading="isLoading"
                  hide-no-data
                  outlined
                  dense
                  item-text="type"
                  label="Item Type"
                  placeholder="Select a type"
                  :rules="[rules.typeRequired]"
                  :prepend-icon="mdiTagText"
                  return-object
                />
              </v-col>

              <v-col cols="12">
                <v-combobox
                  v-if="type === 'list'"
                  v-model="selectedItems"
                  :items="selectedItems"
                  label="Add Options"
                  multiple
                  chips
                  deletable-chips
                  hide-selected
                  clearable
                  outlined
                  dense
                  color="primary"
                  placeholder="Type and press enter to add"
                  :prepend-icon="mdiPlaylistEdit"
                  :rules="[rules.itemRequired]"
                />
              </v-col>
            </v-row>
          </v-form>

          <v-alert v-if="duplicateError" dismisible type="error" class="mt-4"   
                        @click:close="duplicateError = false">
            An item with this name already exists
          </v-alert>
          <v-alert v-if="emptyListError" dismisible type="error" class="mt-4"   
                        @click:close="emptyListError = false">
            List type requires at least one option
          </v-alert>
          <v-alert v-show="errorMessage" dismisible type="error"   
                        @click:close="$emit('update:errorMessage', '')">
            {{ errorMessage }}
          </v-alert>
        </v-card-text>
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import { mdiCreditCardOutline, mdiTagText, mdiPlaylistEdit } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
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
      duplicateError: false,
      emptyListError: false,
      mdiCreditCardOutline,
      mdiTagText,
      mdiPlaylistEdit,
      rules: {
        nameRequired: (v: string) => !!v || 'Name Required',
        nameSize: (v: string) => (!!(v.length < 101)) || 'Name must be less than 101 characters',
        typeRequired: (v: string) => !!v || 'Type Required',
        itemRequired: (v: string[]) => (!!v.length) || 'At least one item required'
      },
      selectedItems: [] as string[],
      name: '',
      type: '',
      types: ['int', 'float', 'bool', 'list']
    }
  },

  methods: {
    async validateAndSave() {
      try {
        // Reset errors
        this.duplicateError = false;
        this.emptyListError = false;

        // Check for duplicate name
        const items = await this.$repositories.perspective.listAllPerspectiveItem();
        const nameExists = items.some(item => 
          item.name.toLowerCase() === this.name.toLowerCase()
        );

        if (nameExists) {
          this.duplicateError = true;
          return;
        }

        // Check if list type has options
        if (this.type === 'list' && !this.selectedItems.length) {
          this.emptyListError = true;
          return;
        }

        // Emit save event if valid
        this.$emit('saveItem', { 
          name: this.name, 
          item_type: this.type, 
          selection_list: this.selectedItems 
        });
      } catch (error) {
        console.error('Error validating item:', error);
        this.duplicateError = true;
      }
    }
  }
})
</script>

<style scoped>
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.v-chip {
  min-width: 36px;
  justify-content: center;
}
</style>
