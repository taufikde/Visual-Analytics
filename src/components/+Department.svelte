<script>

  import RoleTile from "./+RoleTile.svelte";
  import StatTile from "./+StatTile.svelte";
  import AttritionAnalysisChart from "./charts/department/+AttritionAnalysisChart.svelte";
  import PerformanceMatrixChart from "./charts/department/+PerformanceMatrixChart .svelte";
  import CareerProgressionChart from "./charts/department/+CareerProgressionChart .svelte";
  import WorkLifeBalanceHeatmap from "./charts/department/+WorkLifeBalanceHeatmap.svelte";
  import SalaryDistributionChart from "./charts/department/+SalaryDistributionChart .svelte";
	import GenderDiversityChart from "./charts/department/+GenderDiversityChart.svelte";
  
  export let employees = [];

  //unique department names
  let departments = [];
  $: {
    const set = new Set(employees.map((e) => e.Department));
    departments = Array.from(set);
  }

  //Track which department is selected; initially empty
  let selectedDept = '';

  // As soon as `departments` is populated, pick the first one if none is selected
  $: if (departments.length > 0 && !selectedDept) {
    selectedDept = departments[0];
  }

  function selectDept(dept) {
    selectedDept = dept;
  }

    //unique job roles for the selected department
  let roles = [];
  $: {
    if (selectedDept) {
      const filtered = employees.filter((e) => e.Department === selectedDept);
      const roleSet = new Set(filtered.map((e) => e.JobRole));
      roles = Array.from(roleSet);
    } else {
      roles = [];
    }
  }

    //Build a lookup of role → count of employees in that role
  let roleCounts = {};
  $: {
    if (selectedDept) {
      const filtered = employees.filter((e) => e.Department === selectedDept);
      const counts = {};
      filtered.forEach((e) => {
        counts[e.JobRole] = (counts[e.JobRole] || 0) + 1;
      });
      roleCounts = counts;
    } else {
      roleCounts = {};
    }
  }

  // Filter employees by selected department
  let deptEmployees = [];
  $: {
    deptEmployees = selectedDept
      ? employees.filter((e) => e.Department === selectedDept)
      : [];
  }

    // Attrition rate for the selected department
  $: deptAttritionRate = deptEmployees.length
    ? (
        (deptEmployees.filter((e) => e.Attrition === 'Yes').length / deptEmployees.length) *
        100
      ).toFixed(1)
    : 0;

    // Average monthly income for selected department (rounded)
  $: deptAvgIncome = deptEmployees.length
    ? Math.round(deptEmployees.reduce((sum, e) => sum + e.MonthlyIncome, 0) / deptEmployees.length)
    : 0;

  // Percentage of female employees in selected department (rounded %)
  $: deptFemalePercentage = deptEmployees.length
    ? Math.round((deptEmployees.filter((e) => e.Gender === "Female").length / deptEmployees.length) * 100)
    : 0;
</script>

<style>
  /* Add any custom CSS here if needed */
</style>
<div class="space-y-6">
  <!-- 1) Tabs bar -->
  <div class="border-b border-gray-200">
    <nav class="flex overflow-x-auto -mb-px">
      {#each departments as dept}
        <button
          on:click={() => selectDept(dept)}
          class="whitespace-nowrap px-6 py-3 text-sm font-medium transition-colors duration-200
                 {selectedDept === dept
                   ? 'border-b-2 border-blue-600 text-blue-600'
                   : 'border-b-2 border-transparent text-gray-600 hover:text-blue-600 hover:border-blue-300'}"
        >
          {dept}
        </button>
      {/each}
    </nav>
  </div>

  <!-- 2) Content area -->
  <div class="bg-white rounded-2xl shadow p-6">
    {#if selectedDept}
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">
        Department: {selectedDept}
      </h3>

<div class="flex space-x-4 overflow-x-auto py-2 items-stretch">
  
  <!-- Role tiles group -->
  <div class="flex space-x-4">
    {#each roles as role}
      <RoleTile role={role} count={roleCounts[role]} />
    {/each}
  </div>

  <!-- Separator -->
  <div class="border-l border-gray-300 h-auto mx-2"></div>

  <!-- Stat tiles group -->
  <div class="flex space-x-4 px-3">
    <StatTile value={`${deptAttritionRate}%`} label={`Attrition Rate`} />
    <StatTile value={`$${Number(deptAvgIncome).toLocaleString()}`} label="Avg Income" />
    <StatTile value={`${deptFemalePercentage}%`} label={`Female Employees`} />
  </div>
  
</div>
  <!-- Main Charts -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 max-h-[40rem] overflow-y-auto">
        <!-- Attrition Analysis Radar Chart -->
        <div class="lg:col-span-1">
          <AttritionAnalysisChart employees={deptEmployees} selectedDept={selectedDept} />
        </div>
                <!-- Salary Distribution Bubble Chart -->
        <div class="lg:col-span-1">
          <SalaryDistributionChart employees={deptEmployees} selectedDept={selectedDept} />
        </div>

        <!-- Work-Life Balance Heatmap -->
        <div class="lg:col-span-2">
          <WorkLifeBalanceHeatmap employees={deptEmployees} selectedDept={selectedDept} />
        </div>

          <!-- GenderDiversityChart -->
       <div class="lg:col-span-2">
        <GenderDiversityChart employees={deptEmployees} selectedDept={selectedDept} />
      </div>
  </div>
    {:else}
      <!-- This will not appear once departments exist, since we auto-select the first -->
      <p class="text-gray-500">
        No departments available.
      </p>
    {/if}
  </div>
</div>