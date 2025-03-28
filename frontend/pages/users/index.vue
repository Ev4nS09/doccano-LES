<template>
  <v-card>
    <v-card-title v-if="isStaff">
      <v-btn class="text-capitalize" color="primary" @click.stop="$router.push('projects/create')">
        {{ $t('generic.create') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>
    <user-list
      v-model="selected"
      :items="users"
      :is-loading="isLoading"
      :total="users.length"
      @update:query="updateQuery"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import UserList from '@/components/user/UserList.vue'
import FormDelete from '~/components/user/FormDelete.vue'
import { Page } from '~/domain/models/page'
import { Project } from '~/domain/models/project/project'
import { UserItem } from '~/domain/models/user/user'
import { APIUserRepository } from '~/repositories/user/apiUserRepository'
import { SearchQueryData } from '~/services/application/project/projectApplicationService'


export default Vue.extend({


  components: {
    FormDelete,
    UserList,
  },
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogDelete: false,
      users: [] as UserItem [],
      selected: [] as UserItem[],
      isLoading: false
    }
  },

  async fetch() {
            console.error("COnsole log works")
    let query = ''
    let UserAPI = new APIUserRepository(); 
    this.isLoading = true
    this.users = await UserAPI.list(
            query
    )
    this.isLoading = false
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    },

    canClone(): boolean {
      return this.selected.length === 1
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    async remove() {

        let UserAPI = new APIUserRepository(); 
        try
        {
            for(let i = 0; i < this.selected.length; i++)
            {
                await UserAPI.delete(this.selected[i].id)
            }

            this.$fetch()
            this.dialogDelete = false
            this.selected = []
        }
        catch(error)
        {
            console.error("An error occured at remove()")
        }
    },

/*    async clone() {
      const project = await this.$services.project.clone(this.selected[0])
      this.selected = []
      this.$router.push(`/projects/${project.id}/settings`)
    },
*/
    updateQuery(query: object) {
      this.$router.push(query)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
