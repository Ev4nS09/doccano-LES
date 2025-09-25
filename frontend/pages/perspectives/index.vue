<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize mr-2" color="primary" @click.stop="dialogCreate = true">
        {{ "Add Perspective" }}
      </v-btn>
      <v-dialog v-model="dialogCreate">
        <form-create
          v-model="editedPerspective"
          :error-message="errorMessage"
          @cancel="close"
          @save="save"
        />
      </v-dialog>

      <v-btn class="text-capitalize" color="primary" @click.stop="dialogCreateItem = true">
        {{ "Add Item" }}
      </v-btn>
      <v-dialog v-model="dialogCreateItem">
        <FormCreateItem
          v-model="editedPerspectiveItem"
          :error-message="errorMessage"
          @cancelItem="closeItem"
          @saveItem="saveItem"
        />
      </v-dialog>
    </v-card-title>

    <perspective-list
      v-model="selected"
      :items="items"
      :perspective-items="perspectiveItems"
      :is-loading="isLoading"
      :total="items.length"
      :disable-edit="canOnlyAdd"
    />
  </v-card>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import FormCreate from '~/components/perspective/FormCreate.vue'
import FormCreateItem from '~/components/perspective/FormCreateItem.vue'
import { MemberItem } from '~/domain/models/member/member'
 import { Perspective } from '~/domain/models/perspective/perspective'
 import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  components: {
    FormCreate,
    FormCreateItem,
    PerspectiveList,
  },


  layout: 'projects',
  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogCreate: false,
      dialogCreateItem: false,
      dialogDelete: false,
      items: [] as Perspective[],
      editedPerspectiveItem: [] as PerspectiveItem,
      selectedItems: [] as Perspective[],
      perspectiveItems: [] as PerspectiveItem[], 
      createdPerspective: [] as Perspective[],
      selected: [] as Perspective[],
      isLoading: false,
      errorMessage: '',
      tab: 0,
      member: {} as MemberItem,
      editedPerspective: {
        name: '',
        perspectiveItems: [],
      } as Perspective,
    }
  },

  async fetch() {
        this.isLoading = true
        this.items = await this.$repositories.perspective.listPerspective()
        this.perspectiveItems = await this.$repositories.perspective.listAllPerspectiveItem()
        this.isLoading = false
    },

  computed: {

    ...mapGetters('projects', ['project']),

    canOnlyAdd(): boolean {
      if (this.member.isProjectAdmin) {
        return false
      }
      return this.project.allowMemberToCreateLabelType
    },

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

  },
  watch: {
    tab() {
      this.list()
    }
  },

  methods: {
    async list() {
    },
    create() {
        console.error(this.editedPerspective.name)
    },

    async save(data: { name: string; perspectiveItems: number[] }) {
        const perspective = { id: -1, name: data.name, items: data.perspectiveItems as number[], createdAt: '', updatedAt: ''} as Perspective
        await this.$repositories.perspective.createPerspective(perspective)
        this.close()
        this.$fetch()
    },

    close() {
      this.dialogCreate = false
      this.errorMessage = ''
    },

    async saveItem(data: { name: string; item_type: string, selection_list: string[] }) {
        console.error("name: " + data.name + " type: " + data.item_type + " selection_list " + data.selection_list) 
        const perspectiveItem = { 
                id: -1, 
                name: data.name, 
                item_type: data.item_type, 
                selection_list: data.selection_list, 
                createdAt: '', 
                updatedAt: ''
        } as PerspectiveItem
        await this.$repositories.perspective.createPerspectiveItem(perspectiveItem)
        this.closeItem()
        this.$fetch()
    },

    closeItem() {
      this.dialogCreateItem = false
      this.errorMessage = ''
    },
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style> 
