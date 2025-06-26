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
                        display: showAttrition,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Age Range'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Number of Employees'
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
        
        // Create age ranges
        const ageRanges = ['18-25', '26-35', '36-45', '46-55', '56+'];
        
        function getAgeRange(age) {
            if (age <= 25) return '18-25';
            if (age <= 35) return '26-35';
            if (age <= 45) return '36-45';
            if (age <= 55) return '46-55';
            return '56+';
        }
        
        let data;
        if (showAttrition) {
            const ageAttrition = {};
            ageRanges.forEach(range => {
                ageAttrition[range] = { active: 0, left: 0 };
            });
            
            employees.forEach(emp => {
                const range = getAgeRange(emp.Age);
                if (emp.Attrition === 'Yes') {
                    ageAttrition[range].left++;
                } else {
                    ageAttrition[range].active++;
                }
            });
            
            data = {
                labels: ageRanges,
                datasets: [
                    {
                        label: 'Active Employees',
                        data: ageRanges.map(range => ageAttrition[range].active),
                        backgroundColor: '#10B981',
                        borderRadius: 6
                    },
                    {
                        label: 'Left Company',
                        data: ageRanges.map(range => ageAttrition[range].left),
                        backgroundColor: '#EF4444',
                        borderRadius: 6
                    }
                ]
            };
        } else {
            const ageCounts = {};
            ageRanges.forEach(range => ageCounts[range] = 0);
            
            employees.forEach(emp => {
                const range = getAgeRange(emp.Age);
                ageCounts[range]++;
            });
            
            data = {
                labels: ageRanges,
                datasets: [{
                    label: 'Employees',
                    data: Object.values(ageCounts),
                    backgroundColor: '#3B82F6',
                    borderRadius: 6
                }]
            };
        }
        
        chart.data = data;
        chart.options.plugins.legend.display = showAttrition;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Age vs Attrition Analysis' : 'Age Distribution'}
    </h3>
    <div class="h-80">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>