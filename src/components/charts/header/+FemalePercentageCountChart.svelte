<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  // Full employees array
  export let employees = [];
  let overallFemalePct = 40;

  let canvasEl;
  let chart;

  // Reactive calculations
  $: total = employees.length || 1;
  $: femaleCount = employees.filter(e => e.Gender === 'Female').length;
  $: femalePct = Math.round((femaleCount / total) * 100);

  $: femalePctDifference = femalePct - overallFemalePct;

  onMount(() => {
    const ctx = canvasEl.getContext('2d');

    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        // slice for female pct, slice for the remainder
        labels: ['Female %', ''],
        datasets: [{
          data: [femalePct, 100 - femalePct],
          backgroundColor: ['#ec4899', '#e5e7eb'],   // pink for female, transparent remainder
          hoverBackgroundColor: ['#db2777', '#d1d5db']
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

          if (femalePctDifference !== 0) {
              // difference below average
              ctx.font = `${(height / 7).toFixed(2)}px sans-serif`;
              ctx.fillStyle = femalePctDifference > 0 ? '#16a34a' : '#dc2626'; // green or red
              const diffText = `${femalePctDifference > 0 ? '+' : ''}${femalePctDifference}%`;
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
    chart.data.datasets[0].data = [femalePct, 100 - femalePct];
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
  <div class="chart-label">% Female Employees</div>
</div>