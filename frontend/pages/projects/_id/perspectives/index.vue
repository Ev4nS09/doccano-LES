<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize" color="primary" @click.stop="dialogCreate = true">
        {{ $t('generic.add') }}
      </v-btn>
    </v-card-title>
    <perspective-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      :total="items.length"
      :disable-edit="canOnlyAdd"
      @edit="editItem"
    />
  </v-card>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { MemberItem } from '~/domain/models/member/member'
import { ApiPerspectiveRepository } from '@/repositories/perspective/apiPerspectiveRepository'
import { Perspective } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  components: {
    PerspectiveList, 
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      dialogDelete: false,
      items: [] as Perspective[],
      selected: [] as Perspective[],
      isLoading: false,
      tab: 0,
      member: {} as MemberItem
    }
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
  
  async fetch() {
      const API = new ApiPerspectiveRepository()
      this.isLoading = true
        try{
          this.items = await API.list(this.projectId)
        }
        catch{
            console.error("FDS")
        }
      this.isLoading = false
    },

  watch: {
    tab() {
      this.list()
    }
  },

  methods: {
    async list() {
      const API = new ApiPerspectiveRepository()
      this.isLoading = true
      this.items = await API.list(this.projectId)
      this.isLoading = false
    },

    async remove() {
      await this.service.bulkDelete(this.projectId, this.selected)
      this.list()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.service.export(this.projectId)
    },

    editItem(item: LabelDTO) {
      this.$router.push(`labels/${item.id}/edit?type=${this.labelType}`)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
