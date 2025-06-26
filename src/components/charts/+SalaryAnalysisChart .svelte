<script>
    import { onMount, afterUpdate } from 'svelte';
    import { Chart, registerables } from 'chart.js';

    export let employees = [];
    export let showAttrition = false;

    let canvas;
    let chart;
    let prevShowAttrition = showAttrition;

    Chart.register(...registerables);

    // Helper: filter only valid data points
    function valid(emp) {
        return typeof emp.Age === 'number' && !isNaN(emp.Age)
            && typeof emp.MonthlyIncome === 'number' && !isNaN(emp.MonthlyIncome);
    }

    // Chart creation
    function createChart() {
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        chart = new Chart(ctx, {
            type: showAttrition ? 'scatter' : 'line',
            data: { labels: [], datasets: [] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                if (showAttrition) {
                                    return `${context.dataset.label}: Age ${context.parsed.x}, Salary $${context.parsed.y.toLocaleString()}`;
                                }
                                return `${context.dataset.label}: $${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: showAttrition
                        ? {
                            title: { display: true, text: 'Age' },
                            type: 'linear',
                            suggestedMin: 15,
                            suggestedMax: 65
                        }
                        : {
                            title: { display: true, text: 'Job Level' },
                            type: 'category'
                        },
                    y: {
                        title: { display: true, text: 'Monthly Income ($)' },
                        beginAtZero: true,
                        ticks: {
                            callback: value => '$' + value.toLocaleString()
                        }
                    }
                }
            }
        });

        updateChart();
    }

    // Chart update
    function updateChart() {
        if (!chart || employees.length === 0) return;

        if (showAttrition) {
            // Scatter: Age vs Salary, colored by attrition
            const activeEmployees = employees.filter(emp => emp.Attrition === 'No' && valid(emp));
            const leftEmployees = employees.filter(emp => emp.Attrition === 'Yes' && valid(emp));

            chart.data = {
                datasets: [
                    {
                        label: 'Active Employees',
                        data: activeEmployees.map(emp => ({ x: emp.Age, y: emp.MonthlyIncome })),
                        backgroundColor: '#10B981',
                        borderColor: '#10B981',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'Left Company',
                        data: leftEmployees.map(emp => ({ x: emp.Age, y: emp.MonthlyIncome })),
                        backgroundColor: '#EF4444',
                        borderColor: '#EF4444',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }
                ]
            };
        } else {
            // Line: Average salary by job level
            const salaryByLevel = {};
            employees.forEach(emp => {
                if (typeof emp.JobLevel === 'number' && valid(emp)) {
                    if (!salaryByLevel[emp.JobLevel]) {
                        salaryByLevel[emp.JobLevel] = { total: 0, count: 0 };
                    }
                    salaryByLevel[emp.JobLevel].total += emp.MonthlyIncome;
                    salaryByLevel[emp.JobLevel].count++;
                }
            });

            const jobLevels = Object.keys(salaryByLevel)
                .map(Number)
                .sort((a, b) => a - b);

            const avgSalaries = jobLevels.map(level =>
                Math.round(salaryByLevel[level].total / salaryByLevel[level].count)
            );

            chart.data = {
                labels: jobLevels.map(level => `Level ${level}`),
                datasets: [{
                    label: 'Average Monthly Income',
                    data: avgSalaries,
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3B82F6',
                    pointBorderColor: '#3B82F6',
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            };
        }

        chart.update();
    }

    // (Re)create chart if chart type changes
    afterUpdate(() => {
        if (chart && showAttrition !== prevShowAttrition) {
            chart.destroy();
            createChart();
            prevShowAttrition = showAttrition;
        }
    });

    // Initial mount
    onMount(() => {
        createChart();
        return () => {
            if (chart) chart.destroy();
        };
    });

    // Reactivity for data updates
    $: if (chart && employees.length > 0) {
        updateChart();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Salary vs Age (Attrition)' : 'Average Salary by Job Level'}
    </h3>
    <div class="h-80">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>
