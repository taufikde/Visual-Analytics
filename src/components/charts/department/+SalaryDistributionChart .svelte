<script>
  import { onMount, afterUpdate } from 'svelte';
  import * as Chart from 'chart.js';

  export let employees = [];
  export let selectedDept = '';

  let canvasElement;
  let chartInstance;

  Chart.Chart.register(
    Chart.CategoryScale,
    Chart.LinearScale,
    Chart.PointElement,
    Chart.LineElement,
    Chart.Title,
    Chart.Tooltip,
    Chart.Legend,
    Chart.Filler
  );

  function createChart() {
    if (!canvasElement || !employees.length) return;

    if (chartInstance) {
      chartInstance.destroy();
    }

    const roleStats = {};
    employees.forEach(emp => {
      if (!roleStats[emp.JobRole]) {
        roleStats[emp.JobRole] = { salaries: [], ages: [], years: [] };
      }
      roleStats[emp.JobRole].salaries.push(emp.MonthlyIncome);
      roleStats[emp.JobRole].ages.push(emp.Age);
      roleStats[emp.JobRole].years.push(emp.YearsAtCompany);
    });

    const colors = [
      'rgba(99, 102, 241, 0.8)',
      'rgba(16, 185, 129, 0.8)',
      'rgba(245, 158, 11, 0.8)',
      'rgba(239, 68, 68, 0.8)',
      'rgba(139, 92, 246, 0.8)',
      'rgba(236, 72, 153, 0.8)'
    ];

    const datasets = Object.keys(roleStats).map((role, index) => {
      const stats = roleStats[role];
      const avgSalary = stats.salaries.reduce((a, b) => a + b, 0) / stats.salaries.length;
      const avgAge = stats.ages.reduce((a, b) => a + b, 0) / stats.ages.length;
      const count = stats.salaries.length;

      return {
        label: role,
        data: [{
          x: avgAge,
          y: avgSalary,
          r: Math.sqrt(count) * 6 // moderate bubble size
        }],
        backgroundColor: colors[index % colors.length],
        borderColor: colors[index % colors.length].replace('0.8', '1'),
        borderWidth: 2
      };
    });

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'bubble',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Salary vs Age Distribution by Role - ${selectedDept}`,
            font: { size: 16, weight: 'bold' }
          },
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: ctx => {
                const role = ctx.dataset.label;
                const age = ctx.parsed.x.toFixed(1);
                const salary = ctx.parsed.y.toLocaleString();
                const count = Math.round((ctx.parsed.r / 6) ** 2);
                return [
                  `Role: ${role}`,
                  `Avg Age: ${age} years`,
                  `Avg Salary: $${salary}`,
                  `Employees: ${count}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Average Age' },
            grid: { color: 'rgba(0, 0, 0, 0.1)' },
            grace: '10%' // add padding so bubbles near edges are fully visible
          },
          y: {
            title: { display: true, text: 'Average Monthly Income ($)' },
            grid: { color: 'rgba(0, 0, 0, 0.1)' },
            ticks: {
              callback: val => '$' + val.toLocaleString()
            },
            grace: '10%'
          }
        },
        interaction: { intersect: false }
      }
    });
  }

  onMount(() => createChart());
  afterUpdate(() => createChart());
</script>

<style>
  .chart-container {
    width: 100%;
    height: 512px; /* Adjust height as needed */
    position: relative;
  }
  canvas {
    width: 100% !important;
    height: 100% !important;
    display: block;
  }
</style>

<div class="bg-white p-4 rounded-lg shadow-sm border chart-container">
  <canvas bind:this={canvasElement}></canvas>
</div>
