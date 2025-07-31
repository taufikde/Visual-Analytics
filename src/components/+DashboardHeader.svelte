<script>
  import TotalEmployeesChart from "./charts/header/+TotalEmployeesChart.svelte";
  import TotalDepartments from "./charts/header/+TotalDepartments.svelte";
  import JobRolesChart from "./charts/header/+JobRolesChart.svelte";
  import AvgIncomeChart from "./charts/header/+AvgIncomeChart.svelte";
  import FemalePercentageCountChart from "./charts/header/+FemalePercentageCountChart.svelte";
  import AttritionRateCountChart from "./charts/header/+AttritionRateCountChart.svelte";

  import StatTile from "./+StatTile.svelte";
  
  // Props
  export let employees = [];
  export let selectedDept = null;
  export let allEmployees = []; // NEW: We need full dataset for comparisons
  
  // Context-aware title and description
  $: headerTitle = selectedDept ? `${selectedDept} Department Overview` : 'Company Overview';
  $: headerDescription = selectedDept 
    ? `Statistics for ${employees.length} employees in ${selectedDept}`
    : `Statistics for all ${employees.length} employees across ${departmentCount} departments`;
  
  // Reactive calculations based on current employees data (filtered or all)
  $: departmentCount = new Set(employees.map((e) => e.Department)).size;
  $: jobRoleCount = new Set(employees.map((e) => e.JobRole)).size;
  $: attritionRate = employees.length
    ? ((employees.filter((e) => e.Attrition === 'Yes').length / employees.length) * 100).toFixed(1)
    : 0;
  $: avgIncome = employees.length
    ? (employees.reduce((sum, e) => sum + e.MonthlyIncome, 0) / employees.length).toFixed(0)
    : 0;
  $: femalePercentage = employees.length
    ? ((employees.filter((e) => e.Gender === 'Female').length / employees.length) * 100).toFixed(1)
    : 0;

  // NEW: Department-specific metrics (only when viewing single department)
  $: departmentRanking = selectedDept ? calculateDepartmentRanking() : null;
  $: companyAvgIncome = selectedDept ? calculateCompanyAverage() : null;
  $: departmentPerformance = selectedDept ? calculatePerformanceComparison() : null;


  $: deptOvertimeRate = employees.length
    ? ((employees.filter(e => e.OverTime === 'Yes').length / employees.length) * 100).toFixed(1)
    : 0;


  $: companyOvertimeRate = allEmployees.length
    ? ((allEmployees.filter(e => e.OverTime === 'Yes').length / allEmployees.length) * 100).toFixed(1)
    : 0;

  $: deltaOvertime = (deptOvertimeRate - companyOvertimeRate).toFixed(1);
  
  // Helper functions for department-specific insights
  function calculateDepartmentRanking() {
    if (!selectedDept || !allEmployees.length) return null;
    
    const deptSizes = {};
    allEmployees.forEach(emp => {
      deptSizes[emp.Department] = (deptSizes[emp.Department] || 0) + 1;
    });
    
    const sortedDepts = Object.entries(deptSizes)
      .sort(([,a], [,b]) => b - a)
      .map(([dept]) => dept);
    
    return sortedDepts.indexOf(selectedDept) + 1;
  }

  function calculateCompanyAverage() {
    if (!allEmployees.length) return 0;
    return (allEmployees.reduce((sum, e) => sum + e.MonthlyIncome, 0) / allEmployees.length).toFixed(0);
  }

  function calculatePerformanceComparison() {
    if (!selectedDept || !allEmployees.length) return null;
    
    const deptAvg = parseFloat(avgIncome);
    const companyAvg = parseFloat(calculateCompanyAverage());
    const difference = ((deptAvg - companyAvg) / companyAvg * 100).toFixed(1);
    
    return {
      difference: difference,
      isHigher: deptAvg > companyAvg
    };
  }

    $: roleCounts = employees.reduce((acc,e) => {
    acc[e.JobRole] = (acc[e.JobRole]||0) + 1;
    return acc;
  }, {});

  $: sortedRoles = Object.entries(roleCounts)
    .sort(([,a],[,b]) => b - a);

  $: [topRole, topCount] = sortedRoles[0] || ['', 0];
  $: topPct = employees.length
    ? ((topCount / employees.length)*100).toFixed(1)
    : 0;

</script>


<!-- Smart chart grid -->
<div class="flex flex-wrap mb-8">

  <StatTile value={`${employees.length}`} label={`Employees`} />
  
  {#if selectedDept}
    <div class="w-44 h-32 bg-white rounded-2xl mt-2 shadow-sm border mx-2 border-gray-200 hover:shadow-md transition-all duration-200 p-4 flex flex-col justify-center items-center">

        <div class="text-4xl font-bold text-blue-600 mt-2 leading-snug">
          {deptOvertimeRate}%
        </div>

        <div class="text-sm text-gray-500 font-medium mt-1 text-center">
          Overtime Rate
        </div>


       <div class="text-xs text-center mt-1">
          <span
            class="{deltaOvertime > 0 
              ? 'text-green-500' 
              : deltaOvertime < 0 
                ? 'text-red-500' 
                : 'text-gray-500'}"
          >
            {deltaOvertime > 0 ? '+' : ' '}{deltaOvertime}%
          </span> vs. company
        </div>
      </div>
  {:else}
    <!-- For company view: Show total departments -->
       <StatTile value={`${departmentCount}`} label={`Departments`} />
  {/if}
  
  <div class="w-44 h-32 bg-white rounded-2xl mt-2 shadow-sm border mx-2 border-gray-200 hover:shadow-md transition-all duration-200 p-4 flex flex-col justify-center items-center">
    <!-- Big number -->
    <div class="text-lg font-bold text-blue-600 mt-2 leading-snug text-center">
      {topRole}
    </div>
    <!-- Label -->
    <div class="text-sm text-gray-500 font-medium mt-1 text-center">
      Top Role
    </div>
    <!-- Percentage -->
    <div class="mt-1 text-sm text-gray-600 text-center leading-tight">
      <span class=" text-gray-800">{topCount}</span> people
      (<span class=" text-gray-800">{topPct}%</span>)
    </div>
  </div>
  
  <AvgIncomeChart employees={employees} difference={departmentPerformance ? departmentPerformance.difference : 0}/>
  <FemalePercentageCountChart employees={employees}/>
  <AttritionRateCountChart employees={employees} />
</div>