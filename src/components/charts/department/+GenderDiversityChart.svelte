<script>
  import { onMount, afterUpdate } from 'svelte';
  import * as Chart from 'chart.js';

  export let employees = [];
  export let selectedDept = '';

  let canvasElement;
  let chartInstance;

  // Register Chart.js components
  Chart.Chart.register(
    Chart.CategoryScale,
    Chart.LinearScale,
    Chart.BarElement,
    Chart.Title,
    Chart.Tooltip,
    Chart.Legend
  );

  function createChart() {
    if (!canvasElement || !employees.length) return;

    if (chartInstance) {
      chartInstance.destroy();
    }

    // Group employees by department and gender
    const deptGender = {};
    employees.forEach(emp => {
      const dept = emp.Department;
      const gender = emp.Gender;
      if (!deptGender[dept]) {
        deptGender[dept] = { Male: 0, Female: 0, Other: 0 };
      }
      if (gender === 'Male') deptGender[dept].Male++;
      else if (gender === 'Female') deptGender[dept].Female++;
      else deptGender[dept].Other++;
    });

    const labels = Object.keys(deptGender);
    const maleCounts = labels.map(dept => deptGender[dept].Male);
    const femaleCounts = labels.map(dept => deptGender[dept].Female);
    const otherCounts = labels.map(dept => deptGender[dept].Other);

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Male',
            data: maleCounts,
            backgroundColor: 'rgba(59, 130, 246, 0.7)'
          },
          {
            label: 'Female',
            data: femaleCounts,
            backgroundColor: 'rgba(239, 68, 68, 0.7)'
          },
          {
            label: 'Other',
            data: otherCounts,
            backgroundColor: 'rgba(16, 185, 129, 0.7)'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Gender Diversity by Department',
            font: { size: 16, weight: 'bold' }
          },
          legend: {
            position: 'top'
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          x: {
            stacked: true,
            title: {
              display: true,
              text: 'Department'
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Employees'
            }
          }
        }
      }
    });
  }

  onMount(() => {
    createChart();
  });

  afterUpdate(() => {
    createChart();
  });
</script>

<div class="bg-white p-4 rounded-lg shadow-sm border">
  <canvas bind:this={canvasElement} class="w-full h-120"></canvas>
</div>
