<script>
    import { onMount } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    
    export let employees = [];
    export let showAttrition = false;
    
    let canvas;
    let chart;
    
    Chart.register(...registerables);
    
    onMount(() => {
        createChart();
        return () => {
            if (chart) {
                chart.destroy();
            }
        };
    });
    
    $: if (chart && employees.length > 0) {
        updateChart();
    }
    $: if (chart && showAttrition !== undefined) {
        updateChart();
    }
    
    function createChart() {
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'
                    ],
                    borderWidth: 0,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} employees (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '50%'
            }
        });
        
        updateChart();
    }
    
    function updateChart() {
        if (!chart || employees.length === 0) return;
        
        if (showAttrition) {
            // Simple attrition overview
            const attritionCount = employees.filter(emp => emp.Attrition === 'Yes').length;
            const activeCount = employees.length - attritionCount;
            
            chart.data = {
                labels: ['Active Employees', 'Left Company'],
                datasets: [{
                    data: [activeCount, attritionCount],
                    backgroundColor: ['#10B981', '#EF4444'],
                    borderWidth: 0,
                    hoverOffset: 8
                }]
            };
        } else {
            // Department distribution
            const deptCount = {};
            employees.forEach(emp => {
                deptCount[emp.Department] = (deptCount[emp.Department] || 0) + 1;
            });
            
            chart.data = {
                labels: Object.keys(deptCount),
                datasets: [{
                    data: Object.values(deptCount),
                    backgroundColor: [
                        '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'
                    ],
                    borderWidth: 0,
                    hoverOffset: 8
                }]
            };
        }
        
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow-sm p-6 h-92">
    <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-800">
            {showAttrition ? 'Employee Retention' : 'Team Distribution'}
        </h3>
        <div class="text-sm text-gray-500">
            Total: {employees.length} employees
        </div>
    </div>
    <div class="h-64">
        <canvas bind:this={canvas}></canvas>
    </div>
    
    {#if showAttrition}
        <div class="mt-4 text-center">
            <div class="text-2xl font-bold text-gray-800">
                {Math.round(((employees.length - employees.filter(emp => emp.Attrition === 'Yes').length) / employees.length) * 100)}%
            </div>
            <div class="text-sm text-gray-600">Retention Rate</div>
        </div>
    {/if}
</div>