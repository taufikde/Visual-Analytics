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
                plugins: {
                    legend: {
                        position: 'top',
                           labels: {
                                font: {
                                size: 18 
                                }
                            }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Experience Range (Years)',
                             font: {
                                size: 18
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Number of Employees',
                             font: {
                                size: 18
                            }
                        },
                        beginAtZero: true
                    }
                }
            }
        });
        
        updateChart();
    }
    
    function updateChart() {
        if (!chart || employees.length === 0) return;
        
        const experienceRanges = ['0-2', '3-5', '6-10', '11-15', '16+'];
        
        function getExperienceRange(years) {
            if (years <= 2) return '0-2';
            if (years <= 5) return '3-5';
            if (years <= 10) return '6-10';
            if (years <= 15) return '11-15';
            return '16+';
        }
        
        let data;
        if (showAttrition) {
            const expAttrition = {};
            experienceRanges.forEach(range => {
                expAttrition[range] = { active: 0, left: 0 };
            });
            
            employees.forEach(emp => {
                const range = getExperienceRange(emp.TotalWorkingYears);
                if (emp.Attrition === 'Yes') {
                    expAttrition[range].left++;
                } else {
                    expAttrition[range].active++;
                }
            });
            
            data = {
                labels: experienceRanges,
                datasets: [
                    {
                        label: 'Active Employees',
                        data: experienceRanges.map(range => expAttrition[range].active),
                        backgroundColor: '#10B981',
                        borderRadius: 6
                    },
                    {
                        label: 'Left Company',
                        data: experienceRanges.map(range => expAttrition[range].left),
                        backgroundColor: '#EF4444',
                        borderRadius: 6
                    }
                ]
            };
        } else {
            const expCounts = {};
            experienceRanges.forEach(range => expCounts[range] = 0);
            
            employees.forEach(emp => {
                const range = getExperienceRange(emp.TotalWorkingYears);
                expCounts[range]++;
            });
            
            data = {
                labels: experienceRanges,
                datasets: [{
                    label: 'Total Employees',
                    data: Object.values(expCounts),
                    backgroundColor: '#8B5CF6',
                    borderRadius: 6
                }]
            };
        }
        
        chart.data = data;
        chart.options.plugins.legend.display = showAttrition;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6 6 h-92">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Experience vs Attrition' : 'Experience Distribution'}
    </h3>
    <div class="h-64">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>