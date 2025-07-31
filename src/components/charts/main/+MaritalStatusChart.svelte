<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let employees = [];
  export let showAttrition = false;

  let canvas, chart;
  const statuses = ['Single', 'Married', 'Divorced'];
  const colorsTotal = ['#3B82F6','#10B981','#F59E42'];
  const colorsStayed = ['rgba(16,185,129,0.5)','rgba(16,185,129,0.8)','rgba(16,185,129,0.6)'];
  const colorsLeft   = ['rgba(239,68,68,0.5)','rgba(239,68,68,0.8)','rgba(239,68,68,0.6)'];

  onMount(() => {
    chart = new Chart(canvas.getContext('2d'), {
      type: 'polarArea',
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { 
        position: 'bottom',
        labels: {
            font: {
              size: 16 
            }
          }
        }
      
      }
      }
    });
    updateChart();
    return () => chart.destroy();
  });

  $: if (chart) updateChart();

  function updateChart() {
    // count totals & attrition
    const totals = statuses.map(s => employees.filter(e => e.MaritalStatus === s).length);
    const lefts  = statuses.map(s => employees.filter(e => e.MaritalStatus === s && e.Attrition === 'Yes').length);
    const stayed = totals.map((t,i) => t - lefts[i]);

    if (showAttrition) {
      chart.data.datasets = [
        {
          label: 'Stayed',
          data: stayed,
          backgroundColor: colorsStayed,
          borderWidth: 1
        },
        {
          label: 'Left',
          data: lefts,
          backgroundColor: colorsLeft,
          borderWidth: 1
        }
      ];
    } else {
      chart.data.datasets = [
        {
          label: 'Total',
          data: totals,
          backgroundColor: colorsTotal,
          borderWidth: 1
        }
      ];
    }

    chart.data.labels = statuses;
    chart.options.plugins.legend.display = true;
    chart.update();
  }
</script>

<div class="bg-white rounded-2xl shadow p-6 h-92">
  <h3 class="text-xl font-semibold mb-4 text-gray-800">
    {showAttrition ? 'Attrition by Marital Status' : 'Marital Status Distribution'}
  </h3>
  <div class="h-64">
    <canvas bind:this={canvas}></canvas>
  </div>
</div>
