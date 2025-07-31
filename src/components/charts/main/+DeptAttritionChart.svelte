<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let employees = [];
  export let showAttrition = false;

  let canvas, chart;

  onMount(() => {
    createChart();
    return () => chart?.destroy();
  });

  $: if (chart) updateChart();

  function createChart() {
    chart = new Chart(canvas.getContext('2d'), {
      type: showAttrition ? 'bar' : 'pie',
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } }
      }
    });
    updateChart();
  }

  function updateChart() {
    const deptNames = Array.from(new Set(employees.map(e => e.Department)));
    const counts = deptNames.map(d => ({
      total: employees.filter(e => e.Department === d).length,
      left:  employees.filter(e => e.Department === d && e.Attrition === 'Yes').length
    }));

    if (showAttrition) {
      chart.config.type = 'bar';
      chart.data = {
        labels: deptNames,
        datasets: [
          { label: 'Active', data: counts.map(c => c.total - c.left), backgroundColor: '#10B981' },
          { label: 'Left',   data: counts.map(c => c.left),           backgroundColor: '#EF4444' }
        ]
      };
    } else {
      chart.config.type = 'pie';
      chart.data = {
        labels: deptNames,
        datasets: [{
          label: 'Employees',
          data: counts.map(c => c.total),
          backgroundColor: deptNames.map((_, i) => `hsl(${i * 60},60%,60%)`)
        }]
      };
    }

    chart.options.plugins.legend.display = true;
    chart.update();
  }
</script>

<div class="bg-white rounded-2xl shadow p-6 h-92">
  <h3 class="text-xl font-semibold text-gray-800 mb-4">
    {showAttrition ? 'Department Attrition' : 'Employees by Department'}
  </h3>
  <div class="h-64">
    <canvas bind:this={canvas}></canvas>
  </div>
</div>
