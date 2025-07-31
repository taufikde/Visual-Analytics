<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  export let chartOptions;

  let canvasEl;
  let chart;

  onMount(() => {
    if (chart) chart.destroy();

    chart = new Chart(canvasEl, chartOptions);

    return () => {
      chart?.destroy();
    };
  });
</script>

<style>
  .chart-tile-wrapper {
    background-color: white;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
  }

  .chart-container {
    width: 100%;
    height: 220px;
    position: relative;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>

<div class="chart-tile-wrapper">
  <div class="chart-container">
    <canvas bind:this={canvasEl}></canvas>
  </div>
</div>
