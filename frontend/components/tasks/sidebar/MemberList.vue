<template>
  <div class="member-list">
    <v-card class="member-box">
      <v-card-title class="title-section">
        <div>
          <h3 class="title">Dataset Members</h3>
          <p class="subtitle">Current annotation: {{ currentUser }}</p> <!-- Bind to currentUser -->
        </div>
      </v-card-title>

      <v-list class="member-list-content">
        <v-list-item v-for="member in paginatedMembers" :key="member.id" class="member-item">
          <v-btn block text class="member-button" @click="selectUser(member.assignee_username)">
            <div class="member-details">
              <span class="username">{{ member.assignee_username }}</span>
              <span class="role">{{ getRoleForMember(member.assignee_username) }}</span>
            </div>
          </v-btn>
        </v-list-item>
      </v-list>

      <div class="pagination-controls">
        <v-btn icon :disabled="currentPage === 1" @click="prevPage">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z" />
          </svg>
        </v-btn>
        <span class="page-indicator">Página {{ currentPage }} de {{ totalPages }}</span>
        <v-btn icon :disabled="currentPage === totalPages" @click="nextPage">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z" />
          </svg>
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
import { ref, computed, watchEffect, useStore } from '@nuxtjs/composition-api'
import { APIMemberRepository } from '@/repositories/member/apiMemberRepository'

export default {
  name: 'MemberList',
  props: {
    projectId: {
      type: String,
      required: true
    },
    exampleId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const members = ref([])
    const projectMembers = ref([]) // Store project members with roles
    const currentPage = ref(1)
    const itemsPerPage = 5
    const store = useStore() // Access the store
    const currentUser = ref(store.getters['auth/getUsername'] || 'N/A') // Use the getter

    const memberRepository = new APIMemberRepository()

    // Fetch dataset members
    const fetchMembers = async () => {
      try {
        members.value = await memberRepository.listExampleMembers(props.projectId, props.exampleId)
        // Reset currentUser to the logged-in user when dataset changes
        currentUser.value = store.getters['auth/getUsername'] || 'Owner'
      } catch (error) {
        console.error('Failed to fetch dataset members:', error)
      }
    }

    // Fetch project members (to get roles)
    const fetchProjectMembers = async () => {
      try {
        const response = await memberRepository.list(props.projectId)
        projectMembers.value = response
      } catch (error) {
        console.error('Failed to fetch project members:', error)
      }
    }

    // Fetch both dataset and project members when the component is mounted or props change
    watchEffect(() => {
      fetchMembers()
      fetchProjectMembers()
      currentPage.value = 1
    })

    // Get the role for a dataset member based on their username
    const getRoleForMember = (username) => {
      const projectMember = projectMembers.value.find(member => member.username === username)
      return projectMember ? projectMember.rolename : 'N/A' // Return role or 'N/A' if not found
    }

    // Handle user selection
    const selectUser = (username) => {
      currentUser.value = username
    }

    // Pagination logic (unchanged)
    const paginatedMembers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return members.value.slice(start, end)
    })

    const totalPages = computed(() => {
      return Math.ceil(members.value.length / itemsPerPage)
    })

    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++
    }

    return {
      members,
      paginatedMembers,
      currentPage,
      totalPages,
      prevPage,
      nextPage,
      getRoleForMember,
      currentUser, // Expose currentUser to the template
      selectUser // Expose selectUser to the template
    }
  }
}
</script>

<style scoped>
.member-list {
  margin-top: 16px;
}

.member-box {
  border-radius: 4px; /* Rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.title-section {
  padding: 16px; /* Padding inside the box */
  border-bottom: 1px solid rgba(224, 224, 224, 0.05); /* Divider line */
  background-color: #1E1E1E; /* Dark background for title section */
}

.title {
  font-size: 1.25rem; /* 20px */
  font-weight: 500;
  margin-bottom: 4px;
  color: #ffffff; /* White text for contrast */
}

.subtitle {
  font-size: 0.875rem; /* 14px */
  color: #7C7C7C; /* Subtle gray color */
  margin: 0; /* Remove default margin */
}

.member-list-content {
  padding: 8px 0; /* Padding for the list */
}

.member-item {
  padding: 0 16px; /* Remove padding from list item */
}

.member-button {
  display: flex;
  justify-content: flex-start;
  text-transform: none; /* Disable uppercase transformation */
  padding: 8px 16px !important; /* 8px top/bottom, 16px left/right */
  width: 100%; /* Full width */
  min-height: 60px; /* Ensure consistent button height */
  margin: 4px 0; /* Add margin for spacing between buttons */
}

.member-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.username {
  font-size: 1rem; /* 16px */
  font-weight: 600; /* Bold for emphasis */
  margin-bottom: 4px; /* Space between username and role */
  text-transform: capitalize; /* Capitalize first letter only */
  color: #ffffff; /* White text for contrast */
}

.role {
  font-size: 0.875rem; /* 14px */
  color: #7C7C7C; /* Subtle gray color */
  text-transform: capitalize; /* Capitalize first letter only */
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  border-top: 1px solid rgba(224, 224, 224, 0.1); /* Divider line */
}

.page-indicator {
  margin: 0 16px;
  font-size: 0.875rem;
  color: #7C7C7C; /* Subtle gray color */
}

/* Estilo para os botões de navegação */
.v-btn {
  color: #ffffff; /* Cor branca para os ícones */
}

.v-btn:disabled {
  color: rgba(255, 255, 255, 0.3); /* Cor mais clara para botões desabilitados */
}
</style>