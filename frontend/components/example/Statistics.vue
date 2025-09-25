<template>
	<div class="member-list-with-stats" :class="theme">
	  <!-- Label Statistics View -->
	  <div class="content-box">
		<v-card class="stats-box">
		  <v-card-title class="title-section">
			<h3 class="title">Label Statistics</h3>
		  </v-card-title>
  
		  <v-card-text>
			<div v-if="stats" class="stats-container">
			  <p class="total-members">Total Annotators: {{ stats.totalMembers }}</p>
			  <p class="members-with-labels">Annotators: {{ stats.membersWithLabels }}</p>
			  <p class="members-without-labels">
				Abstentions / Skipped: {{ stats.membersWithoutLabels }}</p>
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
  
  export default {
	name: 'Statistics',
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
	  
	  // Label Stats
	  const stats = ref(null);
	  const isLoadingStats = ref(false);
	  const error = ref(null);
	  const currentLabelPage = ref(1);
	  const labelsPerPage = 5;
  
	  const projectService = new ProjectApplicationService($services.project)
	  const agreement_percentage = ref(50.0)
  
	  const { state: labelState, getLabelList } = useLabelList($services.categoryType);
	  const memberRepository = new APIMemberRepository();
  
	  watch(() => props.teacherList, (newVal) => {
		console.log('TeacherList changed, updating stats...', newVal);
		fetchStats();
	  }, { deep: true });
  
	  const fetchLabels = async () => {
		try {
		  await getLabelList(props.projectId);
		} catch (err) {
		  console.error('Failed to fetch labels:', err);
		}
	  };
  
	  watch(() => props.exampleId, (newExampleId, oldExampleId) => {
		console.log(`Example changed from ${oldExampleId} to ${newExampleId}`);
		fetchStats();
	  });
  
	  const fetchMembers = async () => {
		try {
		  members.value = await memberRepository.listExampleMembers(props.projectId, props.exampleId);
		  console.log('Dataset members fetched:', members.value);
		} catch (err) {
		  console.error('Failed to fetch dataset members:', err);
		}
	  };
  
	  const fetchProjectMembers = async () => {
		try {
		  const response = await memberRepository.list(props.projectId);
		  projectMembers.value = response;
		  console.log('Project members fetched:', projectMembers.value);
		} catch (err) {
		  console.error('Failed to fetch project members:', err);
		}
	  };
  
	  const fetchStats = async () => {
		isLoadingStats.value = true;
		error.value = null;
		try {
		  console.log('Fetching statistics...');
		  const data = 
			await memberRepository.fetchMembersWithLabels(props.projectId, props.exampleId);
		  console.log('Fetched Data:', data);
		  stats.value = calculateStats(data);
		} catch (err) {
		  console.error('Failed to fetch statistics:', err);
		  error.value = 'Failed to fetch statistics. Please try again.';
		  stats.value = null;
		} finally {
		  isLoadingStats.value = false;
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
		  labelPercentages[label] 
		  = membersWithLabels > 0 ? (labelCounts[label] / membersWithLabels) * 100 : 0;
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
  
	  const totalLabelPages = computed(() => {
		return Math.ceil(sortedLabels.value.length / labelsPerPage);
	  });
  
	  const paginatedLabels = computed(() => {
		const start = (currentLabelPage.value - 1) * labelsPerPage;
		const end = start + labelsPerPage;
		return sortedLabels.value.slice(start, end);
	  });
  
	  const prevLabelPage = () => {
		if (currentLabelPage.value > 1) currentLabelPage.value--;
	  };
  
	  const nextLabelPage = () => {
		if (currentLabelPage.value < totalLabelPages.value) currentLabelPage.value++;
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
		fetchStats();
		fetchMembers();
		fetchProjectMembers();
		fetchLabels();
		fetchAgreementPercentage();
	  });

	  watch(() => props.exampleId, (newId) => {
		if (newId) {
			stats.value = null;
			fetchStats();
		}
	  }, { immediate: true });
  
	  return {
		members,
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
  
  .title {
	font-size: 1.25rem;
	font-weight: 500;
	margin-bottom: 4px;
	color: var(--text-color);
	margin-right: auto;
  }
  
  .stats-container {
	padding: 4px;
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
  }
  
  .members-with-labels {
	margin-top: 8px; 
	margin-bottom: 4px;
  }
  
  .members-without-labels {
	margin-bottom: 16px;
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