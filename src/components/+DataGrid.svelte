<script>
  import { onMount, onDestroy } from 'svelte';
  import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
  import { createGrid } from 'ag-grid-community';

  ModuleRegistry.registerModules([AllCommunityModule]);

  export let employees = [];
  


  // Define columns
  const columnDefs = [
    { headerName: 'Age', field: 'Age', filter: true },
    { headerName: 'Attrition', field: 'Attrition', filter: true },
    { headerName: 'Business Travel', field: 'BusinessTravel', filter: true },
    { headerName: 'Daily Rate', field: 'DailyRate', filter: true },
    { headerName: 'Department', field: 'Department', filter: true },
    { headerName: 'Distance From Home', field: 'DistanceFromHome', filter: true },
    { headerName: 'Education', field: 'Education', filter: true },
    { headerName: 'Education Field', field: 'EducationField', filter: true },
    { headerName: 'Employee Count', field: 'EmployeeCount', filter: true },
    { headerName: 'Employee Number', field: 'EmployeeNumber', filter: true },
    { headerName: 'Environment Satisfaction', field: 'EnvironmentSatisfaction', filter: true },
    { headerName: 'Gender', field: 'Gender', filter: true },
    { headerName: 'Hourly Rate', field: 'HourlyRate', filter: true },
    { headerName: 'Job Involvement', field: 'JobInvolvement', filter: true },
    { headerName: 'Job Level', field: 'JobLevel', filter: true },
    { headerName: 'Job Role', field: 'JobRole', filter: true },
    { headerName: 'Job Satisfaction', field: 'JobSatisfaction', filter: true },
    { headerName: 'Marital Status', field: 'MaritalStatus', filter: true },
    { headerName: 'Monthly Income', field: 'MonthlyIncome', filter: true },
    { headerName: 'Monthly Rate', field: 'MonthlyRate', filter: true },
    { headerName: 'Num Companies Worked', field: 'NumCompaniesWorked', filter: true },
    { headerName: 'Over 18', field: 'Over18', filter: true },
    { headerName: 'Over Time', field: 'OverTime', filter: true },
    { headerName: 'Percent Salary Hike', field: 'PercentSalaryHike', filter: true },
    { headerName: 'Performance Rating', field: 'PerformanceRating', filter: true },
    { headerName: 'Relationship Satisfaction', field: 'RelationshipSatisfaction', filter: true },
    { headerName: 'Standard Hours', field: 'StandardHours', filter: true },
    { headerName: 'Stock Option Level', field: 'StockOptionLevel', filter: true },
    { headerName: 'Total Working Years', field: 'TotalWorkingYears', filter: true },
    { headerName: 'Training Times Last Year', field: 'TrainingTimesLastYear', filter: true },
    { headerName: 'Work Life Balance', field: 'WorkLifeBalance', filter: true },
    { headerName: 'Years At Company', field: 'YearsAtCompany', filter: true },
    { headerName: 'Years In Current Role', field: 'YearsInCurrentRole', filter: true },
    { headerName: 'Years Since Last Promotion', field: 'YearsSinceLastPromotion', filter: true },
    { headerName: 'Years With Curr Manager', field: 'YearsWithCurrManager', filter: true },
  ];

  let gridDiv;
  let gridApi;

  onMount(() => {
    const gridOptions = {
      columnDefs,
      rowData: employees,
      defaultColDef: {
        sortable: true,
        resizable: true,
        filter: true,
      },
      pagination: true,
      paginationPageSize: 20,
      domLayout: 'autoHeight'
    };

    gridApi = createGrid(gridDiv, gridOptions);

    // Clean up grid instance on destroy
    return () => {
      if (gridApi) {
        gridApi.destroy();
      }
    };
  });

  // If employees prop changes, update the grid data
  $: if (gridApi && employees) {
    gridApi.setGridOption('rowData', employees);
  }
</script>

<div bind:this={gridDiv} class="ag-theme-quartz"></div>
