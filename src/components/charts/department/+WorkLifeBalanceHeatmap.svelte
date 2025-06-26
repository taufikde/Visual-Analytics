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
    
    // Create heatmap data - Work-Life Balance vs Overtime patterns
    const heatmapData = {};
    const workLifeBalanceLabels = ['Poor (1)', 'Fair (2)', 'Good (3)', 'Excellent (4)'];
    const overTimeLabels = ['No Overtime', 'With Overtime'];
    
    // Initialize the heatmap matrix
    workLifeBalanceLabels.forEach((wlb, wlbIndex) => {
      overTimeLabels.forEach((ot, otIndex) => {
        const key = `${wlbIndex}-${otIndex}`;
        heatmapData[key] = {
          x: otIndex,
          y: wlbIndex,
          count: 0,
          attritionCount: 0,
          avgAge: 0,
          avgIncome: 0,
          totalAge: 0,
          totalIncome: 0,
          employees: []
        };
      });
    });

    // Fill the heatmap with employee data
    deptEmployees.forEach(emp => {
      const wlbIndex = (emp.WorkLifeBalance || 1) - 1;
      const otIndex = emp.OverTime === 'Yes' ? 1 : 0;
      const key = `${wlbIndex}-${otIndex}`;
      
      if (heatmapData[key]) {
        heatmapData[key].count++;
        heatmapData[key].totalAge += emp.Age;
        heatmapData[key].totalIncome += emp.MonthlyIncome;
        heatmapData[key].employees.push(emp);
        if (emp.Attrition === 'Yes') {
          heatmapData[key].attritionCount++;
        }
      }
    });

    // Calculate averages and prepare scatter plot data
    const scatterData = [];
    Object.keys(heatmapData).forEach(key => {
      const cell = heatmapData[key];
      if (cell.count > 0) {
        cell.avgAge = cell.totalAge / cell.count;
        cell.avgIncome = cell.totalIncome / cell.count;
        
        // Size represents employee count, color intensity represents attrition rate
        const attritionRate = (cell.attritionCount / cell.count) * 100;
        
        scatterData.push({
          x: cell.x,
          y: cell.y,
          r: Math.max(8, Math.sqrt(cell.count) * 6),
          count: cell.count,
          attritionRate: attritionRate,
          avgAge: cell.avgAge,
          avgIncome: cell.avgIncome,
          wlbLabel: workLifeBalanceLabels[cell.y],
          otLabel: overTimeLabels[cell.x]
        });
      }
    });

    // Create datasets with different colors based on attrition rate
    const lowAttritionData = scatterData.filter(d => d.attritionRate <= 10);
    const mediumAttritionData = scatterData.filter(d => d.attritionRate > 10 && d.attritionRate <= 25);
    const highAttritionData = scatterData.filter(d => d.attritionRate > 25);

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [
          {
            label: 'Low Attrition (≤10%)',
            data: lowAttritionData,
            backgroundColor: 'rgba(34, 197, 94, 0.7)',
            borderColor: 'rgba(34, 197, 94, 1)',
            borderWidth: 2
          },
          {
            label: 'Medium Attrition (11-25%)',
            data: mediumAttritionData,
            backgroundColor: 'rgba(245, 158, 11, 0.7)',
            borderColor: 'rgba(245, 158, 11, 1)',
            borderWidth: 2
          },
          {
            label: 'High Attrition (>25%)',
            data: highAttritionData,
            backgroundColor: 'rgba(239, 68, 68, 0.7)',
            borderColor: 'rgba(239, 68, 68, 1)',
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Work-Life Balance vs Overtime Analysis - ${selectedDept}`,
            font: { size: 16, weight: 'bold' }
          },
          legend: {
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const data = context.raw;
                return [
                  `${data.wlbLabel} & ${data.otLabel}`,
                  `Employees: ${data.count}`,
                  `Attrition Rate: ${data.attritionRate.toFixed(1)}%`,
                  `Avg Age: ${data.avgAge.toFixed(1)} years`,
                  `Avg Income: $${data.avgIncome.toLocaleString()}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            min: -0.5,
            max: 1.5,
            ticks: {
              stepSize: 1,
              callback: function(value) {
                return overTimeLabels[value] || '';
              }
            },
            title: {
              display: true,
              text: 'Overtime Status'
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          y: {
            type: 'linear',
            min: -0.5,
            max: 3.5,
            ticks: {
              stepSize: 1,
              callback: function(value) {
                return workLifeBalanceLabels[value] || '';
              }
            },
            title: {
              display: true,
              text: 'Work-Life Balance Rating'
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
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