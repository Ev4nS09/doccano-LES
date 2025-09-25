
<template>
  <base-card
    :disabled="!valid"
    :title="$t('Item')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('saveItem', { name: name, item_type: type, selection_list: selectedItems })"
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
          :label="('Item Type')"
          :placeholder="('Select a type')"
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
/>      </v-col>
    </v-row>
  </v-form>
</v-card-text>


                    <template #item="props">
            {{ $translateRole(props.item.name, $t('members.roles')) }}
          </template>
          <template #selection="props">
            {{ $translateRole(props.item.name, $t('members.roles')) }}
          </template>
        </v-select>
        <v-alert v-show="errorMessage" prominent type="error">
          <v-row align="center">
            <v-col class="grow">
              {{ errorMessage }}
            </v-col>
          </v-row>
        </v-alert>
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import { mdiAccount, mdiCreditCardOutline, mdiTagText,  mdiPlaylistEdit } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
// import { PerspectiveItem } from '~/domain/models/perspective/perspective'
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
      mdiAccount,
      mdiCreditCardOutline,
      mdiTagText,
      mdiPlaylistEdit,
      rules: {
        nameRequired: (v: string) => (!!v) || 'Name Required',
        nameSize: (v: string) => (!!(v.length < 101)) || 'Name must be less than 101 characters',
        typeRequired: (v: string) => (!!v) || 'Type Required',
        itemRequired: (v: string[]) => (!!v.length) || 'At least one item requeired'
      },
      selectedItems: [] as string[],
      name: '',
      type: '',
      types: ['int', 'float', 'bool', 'list']
    }
  },

  computed: {
  },

  watch: {
    name() {
    }
  },

  async created() {
  }
})
</script>
