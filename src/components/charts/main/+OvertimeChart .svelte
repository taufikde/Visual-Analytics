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
            type: 'bar',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed.x / total) * 100).toFixed(1);
                                return `${context.dataset.label}: ${context.parsed.x} (${percentage}%)`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Number of Employees',
                             font: {
                                size: 18 
                            }
                        },
                        beginAtZero: true
                    },
                    y: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Overtime Status',
                                  font: {
                                size: 18 
                            }
                        }
                    }
                }
            }
        });
        
        updateChart();
    }
    
    function updateChart() {
        if (!chart || employees.length === 0) return;
        
        let data;
        if (showAttrition) {
            // Stacked bar for Overtime and No Overtime with Active and Left
            const overtimeStats = {
                'Overtime': { 'Left': 0, 'Active': 0 },
                'No Overtime': { 'Left': 0, 'Active': 0 }
            };

            employees.forEach(emp => {
                const overtimeKey = emp.OverTime === 'Yes' ? 'Overtime' : 'No Overtime';
                const attritionKey = emp.Attrition === 'Yes' ? 'Left' : 'Active';
                overtimeStats[overtimeKey][attritionKey]++;
            });

            data = {
                labels: ['Overtime', 'No Overtime'],
                datasets: [
                    {
                        label: 'Left',
                        data: [
                            overtimeStats['Overtime']['Left'],
                            overtimeStats['No Overtime']['Left']
                        ],
                        backgroundColor: '#EF4444'
                    },
                    {
                        label: 'Active',
                        data: [
                            overtimeStats['Overtime']['Active'],
                            overtimeStats['No Overtime']['Active']
                        ],
                        backgroundColor: '#10B981'
                    }
                ]
            };
        } else {
            // Simple work pattern distribution
            const overtimeCounts = { 'Yes': 0, 'No': 0 };
            const travelCounts = { 'Travel_Rarely': 0, 'Travel_Frequently': 0, 'Non-Travel': 0 };
            
            employees.forEach(emp => {
                overtimeCounts[emp.OverTime]++;
                travelCounts[emp.BusinessTravel]++;
            });
            
            data = {
                labels: ['Overtime', 'No Overtime', 'Travel Rarely', 'Travel Frequently', 'Non-Travel'],
                datasets: [{
                    label: 'Employee Count',
                    data: [
                        overtimeCounts['Yes'],
                        overtimeCounts['No'],
                        travelCounts['Travel_Rarely'],
                        travelCounts['Travel_Frequently'],
                        travelCounts['Non-Travel']
                    ],
                    backgroundColor: [
                        '#EF4444', '#10B981', '#3B82F6', '#8B5CF6', '#F59E0B'
                    ],
                    borderRadius: 6
                }]
            };

            chart.options.scales.x.stacked = false;
            chart.options.scales.y.stacked = false;
        }

        chart.data = data;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6 h-92">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Overtime & Attrition Analysis' : 'Work Patterns Overview'}
    </h3>
    <div class="h-64">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>
