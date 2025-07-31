<script>
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let employees = [];
  export let difference = 0;

  let canvasEl;
  let chart;

  // Reactive calculations
  $: incomes = employees.map(e => e.MonthlyIncome);
  $: avg = incomes.length ? Math.round(incomes.reduce((a,b) => a + b, 0) / incomes.length) : 0;
  $: max = incomes.length ? Math.max(...incomes) : 0;

  onMount(() => {
    const ctx = canvasEl.getContext('2d');
    
    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Average', 'Remainder'],
        datasets: [{
          data: [avg, Math.max(max - avg, 0)],
          backgroundColor: ['#3b82f6', '#e5e7eb'],
          hoverBackgroundColor: ['#2563eb', '#d1d5db'],
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
          const fontSize = (height / 80).toFixed(2);
          ctx.font = `${fontSize}em sans-serif`;
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#111827';
          
          // Get current average from chart data
          const currentAvg = chart.data.datasets[0].data[0];
          const text = `$${currentAvg.toLocaleString()}`;
          const textX = (width - ctx.measureText(text).width) / 2;
          const textY = height / 2;
          ctx.fillText(text, textX, textY);
        if (difference !== 0) {
                  // difference below average
                  ctx.font = `${(height / 7).toFixed(2)}px sans-serif`;
                  ctx.fillStyle = difference > 0 ? '#16a34a' : '#dc2626'; // green or red
                  const diffText = `${difference > 0 ? '+' : ''}${difference}%`;
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
    chart.data.datasets[0].data = [avg, Math.max(max - avg, 0)];
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
  <div class="chart-label">Avg Monthly Income</div>
</div>