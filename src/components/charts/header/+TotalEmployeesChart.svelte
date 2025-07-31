<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let employees = [];

  let canvasEl;
  let chart;

  onMount(() => {
    const total = employees.length;

    chart = new Chart(canvasEl, {
      type: 'doughnut',
      data: {
        labels: ['Employees', ''],
        datasets: [{
          data: [total, 1],
          backgroundColor: ['#4f46e5', 'rgba(0,0,0,0)'],
          hoverBackgroundColor: ['#4338ca', 'rgba(0,0,0,0)'],
        }]
      },
      options: {
        cutout: '75%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        }
      },
      plugins: [{
        id: 'centerText',
        beforeDraw(chart) {
          const { ctx, width, height } = chart;
          ctx.restore();
          const fontSize = (height / 90).toFixed(2);
          ctx.font = `${fontSize}em sans-serif`;
          ctx.textBaseline = 'middle';
          const text = total.toString();
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
    /* adjust size as needed */
    width: 15rem;
  }
  .chart-container {
    position: relative;
    width: 100%;
    padding-top: 50%; /* 1:1 aspect ratio */
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
  <div class="chart-label">Total Employees</div>
</div>
