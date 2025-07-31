<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';

  // Register all Chart.js components
  Chart.register(...registerables);

  // Full employees array
  export let employees = [];

  let canvasEl;
  let chart;

  onMount(() => {
    // Count unique job roles
    const roleCount = new Set(employees.map(e => e.JobRole)).size;

    // Get 2D drawing context
    const ctx = canvasEl.getContext('2d');

    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Job Roles'],
        datasets: [{
          data: [roleCount],
          backgroundColor: ['#fbbf24'],        // amber ring
          hoverBackgroundColor: ['#f59e0b']
        }]
      },
      options: {
        cutout: '75%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend:  { display: false },
          tooltip: { enabled: false }
        }
      },
      plugins: [{
        id: 'centerText',
        beforeDraw(chart) {
          const { ctx, width, height } = chart;
          ctx.restore();
          // font size relative to height
          const fontSize = (height / 90).toFixed(2);
          ctx.font = `${fontSize}em sans-serif`;
          ctx.textBaseline = 'middle';
          const text = roleCount.toString();
          const textX = (width - ctx.measureText(text).width) / 2;
          const textY = height / 2;
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  });
</script>

<style>
  .chart-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 15rem;              
  }
  .chart-container {
    position: relative;
    width: 100%;
    padding-top: 50%;         
  }
  .chart-container canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
  }
  .chart-label {
    margin-top: 0.5rem;
    font-weight: 500;
    text-align: center;
    width: 100%;
  }
</style>

<div class="chart-wrapper">
  <div class="chart-container">
    <canvas bind:this={canvasEl}></canvas>
  </div>
  <div class="chart-label">Job Roles</div>
</div>
