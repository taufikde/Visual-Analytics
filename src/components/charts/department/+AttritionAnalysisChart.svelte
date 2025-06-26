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
    Chart.PointElement,
    Chart.LineElement,
    Chart.Title,
    Chart.Tooltip,
    Chart.Legend,
    Chart.Filler,
    Chart.RadialLinearScale,
    Chart.ArcElement
  );

  function createChart() {
    if (!canvasElement || !employees.length) return;

    // Destroy existing chart
    if (chartInstance) {
      chartInstance.destroy();
    }

    // Use the employees prop directly (already filtered by parent component)
    const deptEmployees = employees;
    
    // Create age groups and analyze attrition patterns
    const ageGroups = {
      '20-30': { total: 0, attrition: 0 },
      '31-40': { total: 0, attrition: 0 },
      '41-50': { total: 0, attrition: 0 },
      '51-60': { total: 0, attrition: 0 }
    };

    deptEmployees.forEach(emp => {
      let group;
      if (emp.Age <= 30) group = '20-30';
      else if (emp.Age <= 40) group = '31-40';
      else if (emp.Age <= 50) group = '41-50';
      else group = '51-60';

      ageGroups[group].total++;
      if (emp.Attrition === 'Yes') {
        ageGroups[group].attrition++;
      }
    });

    // Calculate attrition rates and prepare data
    const labels = Object.keys(ageGroups);
    const attritionRates = labels.map(group => 
      ageGroups[group].total > 0 
        ? (ageGroups[group].attrition / ageGroups[group].total) * 100 
        : 0
    );
    const totalCounts = labels.map(group => ageGroups[group].total);

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels.map(label => `Age ${label}`),
        datasets: [
          {
            label: 'Attrition Rate (%)',
            data: attritionRates,
            backgroundColor: 'rgba(239, 68, 68, 0.2)',
            borderColor: 'rgba(239, 68, 68, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(239, 68, 68, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(239, 68, 68, 1)',
            fill: true
          },
          {
            label: 'Employee Count (Normalized)',
            data: totalCounts.map(count => (count / Math.max(...totalCounts)) * 100),
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(59, 130, 246, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Attrition Analysis by Age Group - ${selectedDept}`,
            font: { size: 16, weight: 'bold' }
          },
          legend: {
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                if (context.datasetIndex === 0) {
                  return `${context.dataset.label}: ${context.parsed.r.toFixed(1)}%`;
                } else {
                  const actualCount = totalCounts[context.dataIndex];
                  return `Employees: ${actualCount}`;
                }
              }
            }
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            ticks: {
              stepSize: 20
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
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