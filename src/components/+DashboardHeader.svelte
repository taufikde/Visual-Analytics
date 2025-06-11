<script>

  import StatTile from "./+StatTile.svelte";
  // Expect the full employees array as a prop
  export let employees = [];

  // Reactive 
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
</script>

<div class="flex flex-wrap gap-4 mb-8">

  <StatTile value={employees.length} label="Total Employees" />
  <StatTile value={departmentCount} label="Departments" />
  <StatTile value={jobRoleCount} label="Job Roles" />
  <StatTile value={`${attritionRate}%`} label="Attrition Rate" />
  <StatTile value={`$${Number(avgIncome).toLocaleString()}`} label="Avg Monthly Income" />
  <StatTile value={`${femalePercentage}%`} label="% Female Employees" />

</div>
