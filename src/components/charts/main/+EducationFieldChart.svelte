<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let employees = [];
  export let showAttrition = false;

  let canvas, chart;

  onMount(() => {
    chart = new Chart(canvas.getContext('2d'), {
      type: showAttrition ? 'bar' : 'pie',
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: showAttrition ? 'top' : 'bottom',
          labels: {
            font: {
              size: 16 
            }
          }
         } }
      }
    });
    updateChart();
    return () => chart.destroy();
  });

  $: if (chart) updateChart();

  function updateChart() {
    // gather unique fields
    const fields = Array.from(new Set(employees.map(e => e.EducationField)));
    // for each, count total & left
    const totals = fields.map(f => employees.filter(e => e.EducationField === f).length);
    const lefts  = fields.map(f => employees.filter(e => e.EducationField === f && e.Attrition==='Yes').length);

    if (showAttrition) {
      chart.config.type = 'bar';
      chart.data = {
        labels: fields,
        datasets: [
          { label: 'Stayed', data: totals.map((t,i)=>t-lefts[i]), backgroundColor: '#10B981' },
          { label: 'Left',   data: lefts,                              backgroundColor: '#EF4444' }
        ]
      };
    } else {
      chart.config.type = 'pie';
      chart.data = {
        labels: fields,
        datasets: [{
          label: 'Employees',
          data: totals,
          backgroundColor: fields.map((_,i) => `hsl(${i*360/fields.length},60%,60%)`)
        }]
      };
    }

    chart.options.plugins.legend.display = true;
    chart.update();
  }
</script>

<div class="bg-white rounded-2xl shadow p-6 h-92">
  <h3 class="text-xl font-semibold mb-4 text-gray-800">
    {showAttrition ? 'Attrition by Education Field' : 'Education Field Distribution'}
  </h3>
  <div class="h-64">
    <canvas bind:this={canvas}></canvas>
  </div>
</div>
