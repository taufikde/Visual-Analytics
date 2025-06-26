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
    Chart.Filler
  );

  function createChart() {
    if (!canvasElement || !employees.length) return;

    // Destroy existing chart
    if (chartInstance) {
      chartInstance.destroy();
    }

    // Use the employees prop directly (already filtered by parent component)
    const deptEmployees = employees;
    
    // Create performance matrix data
    const performanceData = deptEmployees.map(emp => {
      // Calculate composite satisfaction score
      const satisfactionScore = (
        (emp.JobSatisfaction || 1) +
        (emp.EnvironmentSatisfaction || 1) +
        (emp.RelationshipSatisfaction || 1) +
        (emp.WorkLifeBalance || 1)
      ) / 4;

      // Determine risk level based on multiple factors
      let riskLevel = 0;
      if (emp.Attrition === 'Yes') riskLevel += 3;
      if (emp.OverTime === 'Yes') riskLevel += 1;
      if (emp.DistanceFromHome > 15) riskLevel += 1;
      if (emp.NumCompaniesWorked > 5) riskLevel += 1;
      if (emp.YearsSinceLastPromotion > 3) riskLevel += 1;

      return {
        x: satisfactionScore,
        y: emp.PerformanceRating || 3,
        r: Math.max(5, riskLevel * 3), // Bubble size based on risk
        employee: emp,
        riskLevel: riskLevel
      };
    });

    // Color code by job level
    const colorMap = {
      1: 'rgba(34, 197, 94, 0.7)',   // Green - Entry level
      2: 'rgba(59, 130, 246, 0.7)',  // Blue - Mid level
      3: 'rgba(245, 158, 11, 0.7)',  // Amber - Senior level
      4: 'rgba(239, 68, 68, 0.7)',   // Red - Executive level
      5: 'rgba(139, 92, 246, 0.7)'   // Purple - Top level
    };

    const datasets = [1, 2, 3, 4, 5].map(level => {
      const levelData = performanceData.filter(d => (d.employee.JobLevel || 1) === level);
      return {
        label: `Job Level ${level}`,
        data: levelData,
        backgroundColor: colorMap[level],
        borderColor: colorMap[level].replace('0.7', '1'),
        borderWidth: 2
      };
    }).filter(dataset => dataset.data.length > 0);

    const ctx = canvasElement.getContext('2d');
    chartInstance = new Chart.Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Performance vs Satisfaction Matrix - ${selectedDept}`,
            font: { size: 16, weight: 'bold' }
          },
          legend: {
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const emp = context.raw.employee;
                const satisfaction = context.parsed.x.toFixed(1);
                const performance = context.parsed.y;
                const risk = context.raw.riskLevel;
                return [
                  `Role: ${emp.JobRole}`,
                  `Satisfaction Score: ${satisfaction}/4`,
                  `Performance Rating: ${performance}/4`,
                  `Risk Level: ${risk > 5 ? 'High' : risk > 2 ? 'Medium' : 'Low'}`,
                  `Age: ${emp.Age}, Income: $${emp.MonthlyIncome.toLocaleString()}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Average Satisfaction Score (1-4)'
            },
            min: 0.5,
            max: 4.5,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Performance Rating (1-4)'
            },
            min: 0.5,
            max: 4.5,
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