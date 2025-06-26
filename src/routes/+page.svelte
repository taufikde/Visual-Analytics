<script>
    import Sidebar from '../components/+Sidebar.svelte';
    import Department from '../components/+Department.svelte';
    import DashboardHeader from '../components/+DashboardHeader.svelte';
    import DataGrid from '../components/+DataGrid.svelte';
    
    import DepartmentDistributionChart from '../components/charts/+DepartmentDistributionChart.svelte';
    import AgeDistributionChart from '../components/charts/+AgeDistributionChart .svelte';
    import SalaryAnalysisChart from '../components/charts/+SalaryAnalysisChart .svelte';
    import SatisfactionChart from '../components/charts/+SatisfactionChart .svelte';
    import ExperienceChart from '../components/charts/+ExperienceChart .svelte';
    import OvertimeChart from '../components/charts/+OvertimeChart .svelte';
    
    const { data } = $props();
    const employees = data?.employees ?? [];
    const firstEmployee = employees[0] || {};

    // Track which section is active
    let activeSection = $state('dashboard');
    
    // Track chart view mode - simplified to just two modes
    let showAttritionView = $state(false);


    // Update when Sidebar dispatches "select"
    function onSelectSection(event) {
        activeSection = event.detail;
    }
    
    // Toggle between overview and attrition view
    function toggleView() {
        showAttritionView = !showAttritionView;
    }
</script>

<div class="flex h-screen bg-gray-100">
    
<Sidebar selected={activeSection} on:select={onSelectSection} />

  <!-- Main content area -->
  <main class="flex-1 p-5">
    {#if activeSection === 'dashboard'}
        <div class="mb-6">
            <h2 class="text-3xl font-semibold text-gray-800 mb-4">Dashboard Overview</h2>
        </div>
        
        <DashboardHeader {employees} />
        
        <!-- Charts Section -->
        <div class="mt-6">
            <div class="flex items-center gap-4 mb-6">
                <!-- Overview Button -->
                <button 
                    class="px-4 py-2 rounded-lg font-medium transition-all {showAttritionView ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' : 'bg-blue-600 text-white'}"
                    onclick={() => showAttritionView = false}
                >
                    📊 Overview
                </button>
                <!-- Retention Button -->
                <button 
                    class="px-4 py-2 rounded-lg font-medium transition-all {showAttritionView ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}"
                    onclick={() => showAttritionView = true}
                >
                    📈 Retention
                </button>

            </div>
            <!-- Main Chart -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 max-h-[45rem] overflow-y-auto">
                <!-- Row 1 -->
                <DepartmentDistributionChart {employees} showAttrition={showAttritionView} />
                <AgeDistributionChart {employees} showAttrition={showAttritionView} />

                <!-- Row 2 -->
                <SalaryAnalysisChart {employees} showAttrition={showAttritionView} />
                <SatisfactionChart {employees} showAttrition={showAttritionView} />
                
                <!-- Row 3 -->
                <ExperienceChart {employees} showAttrition={showAttritionView} />
                <OvertimeChart {employees} showAttrition={showAttritionView} />
                
            </div>
        </div>
        
    {:else if activeSection === 'department'}
     <h2 class="text-3xl font-semibold text-gray-800 mb-4">Department</h2>
      <Department {employees} />
    {:else if activeSection === 'datagrid'}
       <h2 class="text-3xl font-bold text-blue-800 mb-6 flex items-center gap-3">
        <span class="inline-block w-2 h-8 rounded bg-blue-400"></span>
            Employee Data Grid
        </h2>

        <div class="bg-white rounded-2xl shadow">
        <DataGrid {employees} />
        </div>
    {/if}
  </main>
</div>