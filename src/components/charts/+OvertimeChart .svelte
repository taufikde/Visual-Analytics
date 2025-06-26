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
                        title: {
                            display: true,
                            text: 'Number of Employees'
                        },
                        beginAtZero: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Categories'
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
            // Overtime vs Attrition analysis
            const analysis = {
                'Overtime + Left': 0,
                'Overtime + Active': 0,
                'No Overtime + Left': 0,
                'No Overtime + Active': 0
            };
            
            employees.forEach(emp => {
                const overtimeStatus = emp.OverTime === 'Yes' ? 'Overtime' : 'No Overtime';
                const attritionStatus = emp.Attrition === 'Yes' ? 'Left' : 'Active';
                const key = `${overtimeStatus} + ${attritionStatus}`;
                analysis[key]++;
            });
            
            data = {
                labels: Object.keys(analysis),
                datasets: [{
                    label: 'Employee Count',
                    data: Object.values(analysis),
                    backgroundColor: [
                        '#EF4444', // Overtime + Left (red)
                        '#F59E0B', // Overtime + Active (orange)
                        '#FCA5A5', // No Overtime + Left (light red)
                        '#10B981'  // No Overtime + Active (green)
                    ],
                    borderRadius: 6
                }]
            };
        } else {
            // Simple overtime distribution
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
        }
        
        chart.data = data;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Overtime & Attrition Analysis' : 'Work Patterns Overview'}
    </h3>
    <div class="h-80">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>