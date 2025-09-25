<template>
  <div class="member-list-with-stats" :class="theme">
    <!-- Buttons for Toggle -->
    <div class="toggle-buttons">
      <v-btn class="toggle-button" :class="{ 'active-button': viewMode === 'label' }" 
      @click="viewMode = 'label'">
        Label Stats
      </v-btn>
      <v-btn class="toggle-button" :class="{ 'active-button': viewMode === 'perspective' }" 
      @click="viewMode = 'perspective'">
        Perspective Stats
      </v-btn>
    </div>

    <!-- Perspective Stats View -->
    <div v-if="viewMode === 'perspective'" class="content-box">
      <v-card class="stats-box">
        <v-card-title class="title-section">
          <v-btn 
            v-if="selectedItem" 
            icon 
            @click="selectedItem = null"
            class="back-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
          </v-btn>
          <h3 class="title">Perspective Statistics</h3>
        </v-card-title>

        <v-card-text>
          <div v-if="perspectiveStats" class="stats-container">
            <p class="total-members">Total Members: {{ perspectiveStats.totalMembers }} </p>
            <p class="members-with-labels">
              Members with Perspective: {{ perspectiveStats.membersWithPerspective }} 
            </p>
            <hr class="divider" />
            <!-- List View -->
            <div v-if="!selectedItem" class="perspective-list-view">
              <div v-for="(item, itemName) in paginatedPerspectiveItems" 
                   :key="itemName" 
                   class="perspective-item-container">
                <v-btn
                  class="perspective-item-button"
                  @click="selectItem(itemName)"
                >
                  <span class="item-name">{{ itemName }}</span>
                </v-btn>
              </div>

              <!-- Perspective Items Pagination Controls -->
              <div class="pagination-controls">
                <v-btn icon :disabled="currentPerspectivePage === 1" @click="prevPerspectivePage">
                  <svg xmlns="http://www.w3.org/2000/svg" 
                  width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z" />
                  </svg>
                </v-btn>
                <span class="page-indicator">
                  Page {{ currentPerspectivePage }} of {{ totalPerspectivePages }}
                </span>
                <v-btn icon :disabled="currentPerspectivePage === totalPerspectivePages" 
                @click="nextPerspectivePage">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z" />
                  </svg>
                </v-btn>
              </div>
            </div>

            <!-- Detail View -->
            <div v-else class="perspective-detail-view">
              <h4 class="selected-item-title">{{ selectedItem }}</h4>
              <div class="value-list">
                <div v-for="(count, valueName) in paginatedValues" 
                     :key="valueName" 
                     class="value-item">
                  <span class="value-name">{{ valueName }}</span>
                  <v-progress-linear
                    :value="(count / perspectiveStats.totalMembers) * 100"
                    :color="getProgressColor((count / perspectiveStats.totalMembers) * 100)"
                    height="20"
                    class="progress-bar"
                  >
                    <strong>{{ count }} 
                      ({{ ((count / perspectiveStats.totalMembers) * 100)
                      .toFixed(2) }}%)</strong>
                  </v-progress-linear>
                </div>
              </div>
              <div class="pagination-controls">
                <v-btn icon :disabled="currentValuePage === 1" @click="prevValuePage">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z" />
                  </svg>
                </v-btn>
                <span class="page-indicator">
                  Page {{ currentValuePage }} of {{ totalValuePages }}
                </span>
                <v-btn icon :disabled="currentValuePage === totalValuePages" @click="nextValuePage">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z" />
                  </svg>
                </v-btn>
              </div>
            </div>
          </div>
          <div v-else-if="isLoadingPerspectiveStats">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p>Loading perspective statistics...</p>
          </div>
          <div v-else>
            <p>Failed to load perspective statistics.</p>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- Label Statistics View -->
    <div v-if="viewMode === 'label'" class="content-box">
      <v-card class="stats-box">
        <v-card-title class="title-section">
          <h3 class="title">Label Statistics</h3>
        </v-card-title>

        <v-card-text>
          <div v-if="stats" class="stats-container">
            <p class="total-members">Total Members: {{ stats.totalMembers }}</p>
            <p class="members-with-labels">Members with Labels: {{ stats.membersWithLabels }}</p>
            <hr class="divider" />

            <div v-for="(item, index) in paginatedLabels" :key="index" 
            class="label-progress-container">
              <p class="label-text">{{ item.label }}</p>
              <v-progress-linear
                :value="item.percentage"
                :color="getProgressColor(item.percentage)"
                height="20"
                class="progress-bar"
              >
                <strong>{{ item.count }} ({{ item.percentage.toFixed(2) }}%)</strong>
              </v-progress-linear>
            </div>
              <!-- Labels Pagination Controls -->
            <div class="pagination-controls">
              <v-btn icon :disabled="currentLabelPage === 1" @click="prevLabelPage">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z" />
                </svg>
              </v-btn>
              <span class="page-indicator">
                Page {{ currentLabelPage }} of {{ totalLabelPages }}
              </span>
              <v-btn icon :disabled="currentLabelPage === totalLabelPages" @click="nextLabelPage">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z" />
                </svg>
              </v-btn>
            </div>
          </div>
          <div v-else-if="isLoadingStats">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p>Loading statistics...</p>
          </div>
          <div v-else>
            <p>Failed to load statistics.</p>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
import { ref, computed, watchEffect, watch, useContext } from '@nuxtjs/composition-api'
import { APIMemberRepository } from '@/repositories/member/apiMemberRepository'
import { useLabelList } from '@/composables/useLabelList'
import { ProjectApplicationService } from '@/services/application/project/projectApplicationService'
import { PerspectiveApplicationService } from '@/services/application/perspective/perspectiveApplicationService'

export default {
  name: 'MemberListWithStats',
  props: {
    projectId: {
      type: String,
      required: true
    },
    exampleId: {
      type: [String, Number],
      required: true
    },
    teacherList: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const { $vuetify, $services } = useContext();
    const theme = computed(() => ($vuetify.theme.dark ? 'dark' : 'light'));

    const members = ref([]);
    const projectMembers = ref([]);
    const viewMode = ref('label'); // 'perspective' or 'label'
    const selectedItem = ref(null);
    
    // Label Stats
    const stats = ref(null);
    const isLoadingStats = ref(false);
    const error = ref(null);
    const currentLabelPage = ref(1);
    const labelsPerPage = 5;
    
    // Perspective Stats
    const perspectiveStats = ref(null);
    const isLoadingPerspectiveStats = ref(false);
    const perspectiveError = ref(null);
    const currentPerspectivePage = ref(1);
    const perspectiveItemsPerPage = 5;
    const selectedItemValues = ref({});
    const currentValuePage = ref(1);
    const valuesPerPage = 5;

    const projectService = new ProjectApplicationService($services.project)
    const perspectiveService = new PerspectiveApplicationService($services.perspective)
    const agreement_percentage = ref(50.0)

    const { state: labelState, getLabelList } = useLabelList($services.categoryType);
    const memberRepository = new APIMemberRepository();

    watch(() => props.teacherList, () => {
      if (viewMode.value === 'label') {
        fetchStats();
      } else if (viewMode.value === 'perspective') {
        fetchPerspectiveStats();
      }
    }, { deep: true });

    const fetchLabels = async () => {
      try {
        await getLabelList(props.projectId);
      } catch (err) {
        console.error('Failed to fetch labels:', err);
      }
    };

    watch(() => props.exampleId, () => {
      
      // Clear previous data
      perspectiveStats.value = null;
      selectedItemValues.value = {};
      selectedItem.value = null;

      if (viewMode.value === 'perspective') {
        fetchPerspectiveStats();
      } else if (viewMode.value === 'label') {
        fetchStats();
      }
    });

    const fetchMembers = async () => {
      try {
        members.value = await memberRepository.listExampleMembers(props.projectId, props.exampleId);
      } catch (err) {
        console.error('Failed to fetch dataset members:', err);
      }
    };

    const fetchProjectMembers = async () => {
      try {
        const response = await memberRepository.list(props.projectId);
        projectMembers.value = response;
      } catch (err) {
        console.error('Failed to fetch project members:', err);
      }
    };

    const fetchStats = async () => {
      isLoadingStats.value = true;
      error.value = null;
      try {
        const data = 
          await memberRepository.fetchMembersWithLabels(props.projectId, props.exampleId);
        stats.value = calculateStats(data);
      } catch (err) {
        console.error('Failed to fetch statistics:', err);
        error.value = 'Failed to fetch statistics. Please try again.';
        stats.value = null;
      } finally {
        isLoadingStats.value = false;
      }
    };

    const fetchPerspectiveStats = async () => {
      isLoadingPerspectiveStats.value = true;
      perspectiveError.value = null;
      try {
        
        // Fetch members data
        const membersData = 
        await memberRepository.listExampleMembers(props.projectId, props.exampleId);
        const totalMembers = membersData.length;

        // Fetch perspective values with proper error handling
        const perspectiveValues = 
        await perspectiveService.listValues(props.projectId, props.exampleId);
        const uniqueUsers = 
        new Set(perspectiveValues.map(v => v.user_name).filter(Boolean));
        const membersWithPerspective = uniqueUsers.size;

        // Get perspective stats
        let perspectiveData = { statistics: {} };
        try {
          perspectiveData = 
          await perspectiveService.getExamplePerspectiveStats(props.projectId, props.exampleId);
        } catch (err) {
          console.log('No perspective stats available, using empty stats');
        }

        perspectiveStats.value = {
          ...perspectiveData,
          totalMembers,
          membersWithPerspective
        };

      } catch (err) {
        console.error('Failed to fetch perspective statistics:', err);
        perspectiveError.value = 'Failed to load perspective statistics.';
        perspectiveStats.value = null;
      } finally {
        isLoadingPerspectiveStats.value = false;
      }
    };

    const selectItem = (itemName) => {
      selectedItem.value = itemName;
      currentValuePage.value = 1;
      if (!selectedItemValues.value[itemName]) {
        try {
          selectedItemValues.value = {
            ...selectedItemValues.value,
            [itemName]: null // Indicates loading
          };
          
          if (perspectiveStats.value?.statistics[itemName]) {
            selectedItemValues.value = {
              ...selectedItemValues.value,
              [itemName]: perspectiveStats.value.statistics[itemName]
            };
          }
        } catch (err) {
          console.error(`Failed to fetch values for item ${itemName}:`, err);
        }
      }
    };

    const calculateStats = (data) => {
      if (!Array.isArray(data)) {
        console.error('Invalid data format:', data);
        return null;
      }

      const totalMembers = data.length;
      const totalLabels = data.reduce((sum, member) => sum + (member.labels?.length || 0), 0);
      const membersWithLabels = data.filter((member) => member.labels?.length > 0).length;
      const membersWithoutLabels = totalMembers - membersWithLabels;

      const labelCounts = {};
      const labelPercentages = {};
      labelState.labels.forEach((label) => {
        labelCounts[label.text] = 0;
        labelPercentages[label.text] = 0;
      });

      data.forEach((member) => {
        if (member.labels && Array.isArray(member.labels)) {
          member.labels.forEach((label) => {
            const labelText = labelState.labels.find((l) => l.id === label)?.text;
            if (labelText) {
              labelCounts[labelText]++;
            }
          });
        }
      });

      Object.keys(labelCounts).forEach((label) => {
        labelPercentages[label] = totalMembers > 0 ? (labelCounts[label] / totalMembers) * 100 : 0;
      });

      return {
        totalMembers,
        totalLabels,
        membersWithLabels,
        membersWithoutLabels,
        labelCounts,
        labelPercentages,
      };
    };

    const getProgressColor = (percentage) => {
      if (percentage >= agreement_percentage.value) {
        return 'green';
      } else if (percentage >= agreement_percentage.value/2) {
        return 'yellow';
      } else {
        return 'red';
      }
    };

    const sortedLabels = computed(() => {
      if (!stats.value || !stats.value.labelPercentages) {
        return [];
      }

      return Object.entries(stats.value.labelPercentages)
        .map(([label, percentage]) => ({ label, 
          percentage, 
          count: stats.value.labelCounts[label] || 0 }))
        .sort((a, b) => b.percentage - a.percentage);
    });

    const perspectiveItems = computed(() => {
      if (!perspectiveStats.value || !perspectiveStats.value.statistics) {
        return [];
      }
      
      return Object.keys(perspectiveStats.value.statistics);
    });

    const totalLabelPages = computed(() => {
      return Math.ceil(sortedLabels.value.length / labelsPerPage);
    });

    const paginatedLabels = computed(() => {
      const start = (currentLabelPage.value - 1) * labelsPerPage;
      const end = start + labelsPerPage;
      return sortedLabels.value.slice(start, end);
    });

    const totalPerspectivePages = computed(() => {
      return Math.ceil(perspectiveItems.value.length / perspectiveItemsPerPage);
    });

    const paginatedPerspectiveItems = computed(() => {
      const start = (currentPerspectivePage.value - 1) * perspectiveItemsPerPage;
      const end = start + perspectiveItemsPerPage;
      const items = {};
      
      perspectiveItems.value.slice(start, end).forEach(itemName => {
        items[itemName] = perspectiveStats.value.statistics[itemName];
      });
      
      return items;
    });

    const totalValuePages = computed(() => {
      if (!selectedItem.value || !selectedItemValues.value[selectedItem.value]) {
        return 0;
      }
      return Math.ceil(
        Object.keys(selectedItemValues.value[selectedItem.value]).length / valuesPerPage
      );
    });

    const paginatedValues = computed(() => {
      if (!selectedItem.value || !selectedItemValues.value[selectedItem.value]) {
        return {};
      }
      
      const start = (currentValuePage.value - 1) * valuesPerPage;
      const end = start + valuesPerPage;
      const values = selectedItemValues.value[selectedItem.value];
      const entries = Object.entries(values);
      
      return Object.fromEntries(entries.slice(start, end));
    });

    const prevValuePage = () => {
      if (currentValuePage.value > 1) currentValuePage.value--;
    };

    const nextValuePage = () => {
      if (currentValuePage.value < totalValuePages.value) currentValuePage.value++;
    };

    const prevLabelPage = () => {
      if (currentLabelPage.value > 1) currentLabelPage.value--;
    };

    const nextLabelPage = () => {
      if (currentLabelPage.value < totalLabelPages.value) currentLabelPage.value++;
    };

    const prevPerspectivePage = () => {
      if (currentPerspectivePage.value > 1) currentPerspectivePage.value--;
    };

    const nextPerspectivePage = () => {
      if (currentPerspectivePage.value < totalPerspectivePages.value) 
        currentPerspectivePage.value++;
    };

    const fetchAgreementPercentage = async () => {
      try {
        agreement_percentage.value = await projectService.getAgreementPercentage(
          Number(props.projectId))
      } catch (error) {
        console.error('Failed to fetch agreement percentage:', error)
      }
    }

    watchEffect(() => {
      if (viewMode.value === 'label') {
        fetchStats();
      } else if (viewMode.value === 'perspective') {
        fetchPerspectiveStats();
      }
      
      fetchMembers();
      fetchProjectMembers();
      fetchLabels();
      fetchAgreementPercentage();
    });

    return {
      members,
      viewMode,
      stats,
      isLoadingStats,
      error,
      theme,
      labelState,
      getProgressColor,
      sortedLabels,
      paginatedLabels,
      currentLabelPage,
      totalLabelPages,
      prevLabelPage,
      nextLabelPage,
      perspectiveStats,
      isLoadingPerspectiveStats,
      perspectiveItems,
      paginatedPerspectiveItems,
      currentPerspectivePage,
      totalPerspectivePages,
      prevPerspectivePage,
      nextPerspectivePage,
      selectedItemValues,
      selectedItem,
      selectItem,
      currentValuePage,
      totalValuePages,
      paginatedValues,
      prevValuePage,
      nextValuePage
    };
  },
}
</script>

<style scoped>
.member-list-with-stats {
  margin-top: 16px;
  background-color: var(--background-color);
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.toggle-buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.toggle-button {
  flex: 1;
  background-color: var(--button-background);
  color: var(--text-color);
  transition: background-color 0.3s ease;
}

.toggle-button.active-button {
  background-color: var(--button-background);
  color: var(--text-light);
  border-color: var(--button-background);
}

.content-box {
  background-color: var(--background-color);
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stats-box {
  border-radius: 4px;
  background-color: var(--background-color);
}

.title-section {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
}

.back-button {
  margin-right: auto;
}

.title {
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--text-color);
  margin-right: auto;
}

.subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

.stats-container {
  padding: 4px;
}

.perspective-list-view {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.perspective-item-container {
  margin-bottom: 8px;
}

.perspective-item-button {
  width: 100%;
  justify-content: flex-start;
  text-transform: none;
  padding: 12px 16px;
}

.selected-item-title {
  margin-bottom: 16px;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-color);
}

.perspective-detail-view {
  padding: 8px;
}

.item-name {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-color);
}

.value-list {
  margin-top: 8px;
}

.value-item {
  margin-bottom: 12px;
}

.value-name {
  display: block;
  margin-bottom: 4px;
  font-size: 0.875rem;
  color: var(--text-color);
}

.loading-values {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  border-top: 1px solid var(--border-color);
}

.page-indicator {
  margin: 0 16px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.v-btn {
  color: var(--text-color);
}

.v-btn:disabled {
  color: var(--text-disabled);
}

.v-progress-linear {
  margin-top: 8px;
  margin-bottom: 16px;
}

.v-progress-linear strong {
  font-size: 0.875rem;
  color: var(--text-color);
}

.total-members {
  margin-top: 8px;
  margin-bottom: 4px;
  color: var(--text-color);
}

.members-with-labels {
  margin-bottom: 16px;
  color: var(--text-color);
}

.divider {
  margin-top: 16px;
  margin-bottom: 16px;
  border-color: var(--border-color);
}

.label-progress-container {
  margin-bottom: 8px;
}

.label-text {
  margin-bottom: 4px;
  color: var(--text-color);
}

.progress-bar {
  margin-top: 4px;
}

/* Dark Theme */
.member-list-with-stats.dark {
  --background-color: #1E1E1E;
  --button-background: #1d1c1c;
  --text-color: #FFFFFF;
  --text-secondary: #7C7C7C;
  --text-light: #FFFFFF;
  --text-disabled: rgba(255, 255, 255, 0.3);
  --border-color: rgba(224, 224, 224, 0.1);
  --hover-background: rgba(255, 255, 255, 0.05);
}

/* Light Theme */
.member-list-with-stats.light {
  --background-color: #FFFFFF;
  --button-background: #F5F5F5;
  --text-color: #000000;
  --text-secondary: #555555;
  --text-light: #FFFFFF;
  --text-disabled: rgba(0, 0, 0, 0.3);
  --border-color: rgba(0, 0, 0, 0.1);
  --hover-background: rgba(0, 0, 0, 0.05);
}
</style>