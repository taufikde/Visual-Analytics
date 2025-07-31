<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  // Full employees array
  export let employees = [];
  let overallAttritionPct = 16;

  let canvasEl;
  let chart;

  // Reactive calculations
  $: total = employees.length || 1;
  $: attrited = employees.filter(e => e.Attrition === 'Yes').length;
  $: attritionPct = Math.round((attrited / total) * 100);

  $: attritionPctDifference = attritionPct - overallAttritionPct;

  onMount(() => {
    const ctx = canvasEl.getContext('2d');

    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        // slice for attrition, remainder transparent
        labels: ['Attrition', ''],
        datasets: [{
          data: [attritionPct, 100 - attritionPct],
          backgroundColor: ['#ef4444', '#e5e7eb'],   // red ring
          hoverBackgroundColor: ['#dc2626', '#d1d5db']
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
          const fontSize = (height / 90).toFixed(2);
          ctx.font = `${fontSize}em sans-serif`;
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#111827';
          
          // Get current percentage from chart data
          const currentPct = chart.data.datasets[0].data[0];
          const text = `${currentPct}%`;
          const textX = (width - ctx.measureText(text).width) / 2;
          const textY = height / 2;
          ctx.fillText(text, textX, textY);

          if (attritionPctDifference !== 0) {
              // difference below average
              ctx.font = `${(height / 7).toFixed(2)}px sans-serif`;
              ctx.fillStyle = attritionPctDifference > 0 ? '#16a34a' : '#dc2626'; // green or red
              const diffText = `${attritionPctDifference > 0 ? '+' : ''}${attritionPctDifference}%`;
              const diffTextWidth = ctx.measureText(diffText).width;
              const diffTextX = (width - diffTextWidth) / 2;
              const diffTextY = height / 2 + 28;
              ctx.fillText(diffText, diffTextX, diffTextY);
        }
          ctx.save();
        }
      }]
    });
  });

  // KEY FIX: Update chart when employees data changes
  $: if (chart && employees.length) {
    // Update chart data
    chart.data.datasets[0].data = [attritionPct, 100 - attritionPct];
    // Trigger chart update
    chart.update();
  }

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<style>
  .chart-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 15rem;              /* match your other tiles */
  }
  .chart-container {
    position: relative;
    width: 100%;
    padding-top: 50%;          /* maintains the aspect ratio */
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
  <div class="chart-label">Attrition Rate</div>
</div>