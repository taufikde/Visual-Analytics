<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let employees = [];

  let canvas, chart;

  onMount(() => {
    const ctx = canvas.getContext('2d');
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Avg Rating'], // now shows label on y-axis
        datasets: [
          {
            label: 'Max Rating',
            data: [4],
            backgroundColor: '#E5E7EB',
            barThickness: 32,
            categoryPercentage: 0.8,
          },
          {
            label: 'Employee Avg',
            data: [
              employees.length
                ? employees.reduce((sum, e) => sum + e.PerformanceRating, 0) / employees.length
                : 0
            ],
            backgroundColor: '#3B82F6',
            barThickness: 32,
            categoryPercentage: 0.8,
          }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false
           },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(2)}`
            }
          }
        },
        scales: {
          x: {
            min: 0,
            max: 4,
            ticks: {
              stepSize: 1,
              color: '#6B7280',
              font: { size: 10 }
            },
            grid: { display: false },
   /*         title: {
              display: true,
              text: 'Performance Rating',
              color: '#374151',
              font: { size: 14 }
            }
              */
          },
          y: {
            ticks: {
              color: '#6B7280',
              font: { size: 16 }
            },
            grid: { display: false }
          }
        }
      }
    });

    return () => chart.destroy();
  });
</script>

<style>
  .chart-wrapper {
    width: 100%;
    height: 4rem;
    position: relative;
  }
  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>

<div class="bg-white rounded-2xl shadow p-4 flex flex-col justify-center">
  <div class="text-center text-sm text-gray-600 mb-2">Performance Rating</div>
  <div class="text-center text-xl font-bold text-blue-600 mb-3">
    {employees.length 
      ? (employees.reduce((s, e) => s + e.PerformanceRating, 0) / employees.length).toFixed(2)
      : '0.00'}
  </div>
  <div class="chart-wrapper">
    <canvas bind:this={canvas}></canvas>
  </div>
</div>
