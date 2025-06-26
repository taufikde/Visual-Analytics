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
    Chart.ArcElement,
    Chart.Title,
    Chart.Tooltip,
    Chart.Legend
  );

  function createChart() {
    if (!canvasElement || !employees.length) return;

    // Destroy existing chart
    if (chartInstance) {
      chartInstance.destroy();
    }

    // Use the employees prop directly (already filtered by parent component)
    const deptEmployees = employees;
    
    // Analyze career progression patterns
    const progressionData = {};
    
    deptEmployees.forEach(emp => {
      const key = `${emp.JobLevel || 1}-${emp.YearsAtCompany || 0}`;
      const experienceCategory = 
        emp.YearsAtCompany <= 2 ? 'New (0-2 years)' :
        emp.YearsAtCompany <= 5 ? 'Experienced (3-5 years)' :
        emp.YearsAtCompany <= 10 ? 'Senior (6-10 years)' :
        'Veteran (10+ years)';
      
      const levelCategory = `Level ${emp.JobLevel || 1}`;
      
      if (!progressionData[experienceCategory]) {
        progressionData[experienceCategory] = {};
      }
      if (!progressionData[experienceCategory][levelCategory]) {
        progressionData[experienceCategory][levelCategory] = 0;
      }
      progressionData[experienceCategory][levelCategory]++;
    });

    // Create nested doughnut chart data
    const experienceCategories = Object.keys(progressionData);
    const colors = [
      ['rgba(34, 197, 94, 0.8)', 'rgba(34, 197, 94, 0.6)', 'rgba(34, 197, 94, 0.4)', 'rgba(34, 197, 94, 0.2)'],
      ['rgba(59, 130, 246, 0.8)', 'rgba(59, 130, 246, 0.6)', 'rgba(59, 130, 246, 0.4)', 'rgba(59, 130, 246, 0.2)'],
      ['rgba(245, 158, 11, 0.8)', 'rgba(245, 158, 11, 0.6)', 'rgba(245, 158, 11, 0.4)', 'rgba(245, 158, 11, 0.2)'],
      ['rgba(239, 68, 68, 0.8)', 'rgba(239, 68, 68, 0.6)', 'rgba(239, 68, 68, 0.4)', 'rgba(239, 68, 68, 0.2)']
    ];

    // Outer ring - Experience categories
    const outerData = [];
    const outerLabels = [];
    const outerColors = [];

    experienceCategories.forEach((expCat, expIndex) => {
      const total = Object.values(progressionData[expCat]).reduce((sum, count) => sum + count, 0);
      outerData.push(total);
      outerLabels.push(expCat);
      outerColors.push(colors[expIndex % colors.length][0]);
    });

    // Inner ring - Job levels within each experience category
    const innerData = [];
    const innerLabels = [];
    const innerColors = [];

    experienceCategories.forEach((expCat, expIndex) => {
      const levels = Object.keys(progressionData[expCat]).sort();
      levels.forEach((level, levelIndex) => {
        innerData.push(progressionData[expCat][level]);
        innerLabels.push(`${expCat} - ${level}`);
        innerColors.push(colors[expIndex % colors.length][levelIndex % 4]);
      });
    });

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: innerLabels,
        datasets: [
          {
            label: 'Experience Categories',
            data: outerData,
            backgroundColor: outerColors,
            borderColor: outerColors.map(color => color.replace('0.8', '1')),
            borderWidth: 2,
            cutout: '20%',
            radius: '60%'
          },
          {
            label: 'Job Levels',
            data: innerData,
            backgroundColor: innerColors,
            borderColor: innerColors.map(color => color.replace(/0\.\d/, '1')),
            borderWidth: 1,
            cutout: '60%',
            radius: '90%'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Career Progression Analysis - ${selectedDept}`,
            font: { size: 16, weight: 'bold' }
          },
          legend: {
            position: 'right',
            labels: {
              generateLabels: function(chart) {
                const original = Chart.Chart.defaults.plugins.legend.labels.generateLabels;
                const labels = original.call(this, chart);
                
                // Combine both datasets into one legend
                const combinedLabels = [];
                
                // Add experience categories
                outerLabels.forEach((label, index) => {
                  combinedLabels.push({
                    text: label,
                    fillStyle: outerColors[index],
                    strokeStyle: outerColors[index],
                    lineWidth: 2,
                    datasetIndex: 0,
                    index: index
                  });
                });
                
                return combinedLabels;
              }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label;
                const value = context.parsed;
                const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} employees (${percentage}%)`;
              }
            }
          }
        },
        interaction: {
          intersect: false
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