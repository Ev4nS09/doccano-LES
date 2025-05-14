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
    />
  </v-card>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import { MemberItem } from '~/domain/models/member/member'
 import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export default Vue.extend({
  components: {
    PerspectiveList,
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      dialogDelete: false,
      items: [] as PerspectiveItem[],
      selected: [] as PerspectiveItem[],
      isLoading: false,
      tab: 0,
      member: {} as MemberItem
    }
  },

  async fetch() {
        this.isLoading = true
        this.items = await this.$repositories.perspective.list(this.projectId)
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

  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
