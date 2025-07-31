<script>
    import RoleTile from '../components/+RoleTile.svelte';
    import StatTile from '../components/+StatTile.svelte';
    import Sidebar from '../components/+Sidebar.svelte';


    import DashboardHeader from '../components/+DashboardHeader.svelte';
    import DataGrid from '../components/+DataGrid.svelte';
    
    import MaritalStatusChart from '../components/charts/main/+MaritalStatusChart.svelte';
    import EducationFieldChart from '../components/charts/main/+EducationFieldChart.svelte';
    import DepartmentDistributionChart from '../components/charts/main/+DepartmentDistributionChart.svelte';
    import AgeDistributionChart from '../components/charts/main/+AgeDistributionChart .svelte';
    import SatisfactionChart from '../components/charts/main/+SatisfactionChart .svelte';
    import ExperienceChart from '../components/charts/main/+ExperienceChart .svelte';
    import OvertimeChart from '../components/charts/main/+OvertimeChart .svelte';
    import PerformanceBulletChart from '../components/charts/main/+PerformanceBulletChart.svelte';
    import TopEmployeesDashboard from '../components/+TopEmployeesDashboard.svelte';

    
    const { data } = $props(); 
    const employees = data?.employees ?? [];
    const topEmployees =  data?.topEmployees ?? [];
    const firstEmployee = employees[0] || {};

    
     const departments = [...new Set(employees.map(e => e.Department))];

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

    let selectedDept = $state(null);

    function selectDept(dept) {
        selectedDept = dept;
 
        if (dept) {
        // When a specific department is selected, turn on attrition view
        if (!showAttritionView) toggleView();
        } else {
            // When "All departments" is selected (null), turn it off
            if (showAttritionView) toggleView();
        }
    }

    let roles = $derived(
    selectedDept
        ? Array.from(
            new Set(
            employees
                .filter(e => e.Department === selectedDept)
                .map(e => e.JobRole)
            )
        )
        : []
    );

    let roleCounts = $derived(
    selectedDept
        ? employees
            .filter(e => e.Department === selectedDept)
            .reduce((acc, e) => {
            acc[e.JobRole] = (acc[e.JobRole] || 0) + 1;
            return acc;
            }, {})
        : {}
    );

    let deptEmployees = $derived(
    selectedDept
        ? employees.filter(e => e.Department === selectedDept)
        : []
    );

      // NEW: Derived value for employees to show in header (filtered or all)
    let displayEmployees = $derived(
        selectedDept ? deptEmployees : employees
    );

</script>

<div class="flex h-screen bg-gray-50">
    
<Sidebar selected={activeSection} on:select={onSelectSection} />

  <!-- Main content area -->
  <main class="flex-1 p-3">
    {#if activeSection === 'dashboard'}

     <!-- Tabs bar -->
        <nav class="flex overflow-x-auto border-b border-blue-600">
        <button
            class="px-4 py-2 mr-2 rounded-t-md {selectedDept === null ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
            onclick={() => selectDept(null)}
        >
            All Depts
        </button>
        {#each departments as dept}
            <button
            class="px-4 py-2 mr-2 rounded-t-md {selectedDept === dept ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
            onclick= {() => selectDept(dept)}
            >
            {dept}
            </button>
        {/each}
        </nav>
        <section class="my-6">
            <DashboardHeader 
                employees={displayEmployees} 
                selectedDept={selectedDept} 
                allEmployees={employees} 
            />
        </section>

        
    <!-- 2) Department selector -->
    <section class="space-y-4">
       
        <div>     
            {#if selectedDept}
              <!--    <div class="flex">
                    <div class="flex space-x-4 overflow-x-auto py-2 items-stretch">
                    <div class="flex space-x-4">
                        {#each roles as role}
                            <RoleTile role={role} count={roleCounts[role]} />
                        {/each}
                    </div>
                </div> 
            </div>  -->
             <div class="grid grid-cols-4 gap-6 mt-4">
                <AgeDistributionChart employees={displayEmployees} showAttrition={showAttritionView}/>
                <SatisfactionChart  employees={displayEmployees} showAttrition={showAttritionView} />

                 <ExperienceChart employees={displayEmployees} showAttrition={showAttritionView} />
                <OvertimeChart employees={displayEmployees} showAttrition={showAttritionView} />

             </div>

              <TopEmployeesDashboard {topEmployees} {employees} {selectedDept}/>
             {:else}
                <!-- Main Chart  -->
                <div class="grid grid-cols-4 gap-6">
                    <DepartmentDistributionChart {employees} showAttrition={showAttritionView} />
                    <AgeDistributionChart {employees} showAttrition={showAttritionView} />
                    <SatisfactionChart {employees} showAttrition={showAttritionView} />
                    <ExperienceChart {employees} showAttrition={showAttritionView} />
                    <OvertimeChart {employees} showAttrition={showAttritionView} />
                    <MaritalStatusChart   {employees} showAttrition={showAttritionView} />
                    <EducationFieldChart  {employees} showAttrition={showAttritionView} />
                    <PerformanceBulletChart {employees} showAttrition={showAttritionView} />
                    
                </div>

            {/if}
            </div>
    </section>
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