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
            type: 'radar',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 4,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
        
        updateChart();
    }
    
    function updateChart() {
        if (!chart || employees.length === 0) return;
        
        const satisfactionMetrics = [
            'Job Satisfaction',
            'Environment Satisfaction',
            'Work Life Balance',
            'Relationship Satisfaction',
            'Job Involvement'
        ];
        
        function getAverageRatings(employeeList) {
            const totals = {
                JobSatisfaction: 0,
                EnvironmentSatisfaction: 0,
                WorkLifeBalance: 0,
                RelationshipSatisfaction: 0,
                JobInvolvement: 0
            };
            
            employeeList.forEach(emp => {
                totals.JobSatisfaction += emp.JobSatisfaction;
                totals.EnvironmentSatisfaction += emp.EnvironmentSatisfaction;
                totals.WorkLifeBalance += emp.WorkLifeBalance;
                totals.RelationshipSatisfaction += emp.RelationshipSatisfaction;
                totals.JobInvolvement += emp.JobInvolvement;
            });
            
            const count = employeeList.length;
            return [
                totals.JobSatisfaction / count,
                totals.EnvironmentSatisfaction / count,
                totals.WorkLifeBalance / count,
                totals.RelationshipSatisfaction / count,
                totals.JobInvolvement / count
            ];
        }
        
        let data;
        if (showAttrition) {
            const activeEmployees = employees.filter(emp => emp.Attrition === 'No');
            const leftEmployees = employees.filter(emp => emp.Attrition === 'Yes');
            
            data = {
                labels: satisfactionMetrics,
                datasets: [
                    {
                        label: 'Active Employees',
                        data: getAverageRatings(activeEmployees),
                        borderColor: '#10B981',
                        backgroundColor: 'rgba(16, 185, 129, 0.2)',
                        pointBackgroundColor: '#10B981',
                        pointBorderColor: '#10B981',
                        pointRadius: 4
                    },
                    {
                        label: 'Left Company',
                        data: getAverageRatings(leftEmployees),
                        borderColor: '#EF4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.2)',
                        pointBackgroundColor: '#EF4444',
                        pointBorderColor: '#EF4444',
                        pointRadius: 4
                    }
                ]
            };
        } else {
            data = {
                labels: satisfactionMetrics,
                datasets: [{
                    label: 'Average Satisfaction Ratings',
                    data: getAverageRatings(employees),
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    pointBackgroundColor: '#3B82F6',
                    pointBorderColor: '#3B82F6',
                    pointRadius: 4
                }]
            };
        }
        
        chart.data = data;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Satisfaction Ratings (Attrition Comparison)' : 'Employee Satisfaction Overview'}
    </h3>
    <div class="h-80">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>