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
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 18 
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: false,
                        min: 1,
                        max: 4,
                        ticks: {
                            stepSize: 4,
                            font: {
                                size: 18 
                            },
                            // Custom tick labels to show 1, 2, 3, 4
                            callback: function(value) {
                                return value;
                            }
                        },
                        pointLabels: {
                            font: {
                                size: 16 
                            }
                        },
                        // Add grid lines for better visibility
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        // Customize the angle lines
                        angleLines: {
                            color: 'rgba(0, 0, 0, 0.1)'
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
                Math.round((totals.JobSatisfaction / count) * 100) / 100,
                Math.round((totals.EnvironmentSatisfaction / count) * 100) / 100,
                Math.round((totals.WorkLifeBalance / count) * 100) / 100,
                Math.round((totals.RelationshipSatisfaction / count) * 100) / 100,
                Math.round((totals.JobInvolvement / count) * 100) / 100
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
                        label: 'Active Emp. Rating',
                        data: getAverageRatings(activeEmployees),
                        borderColor: '#10B981',
                        backgroundColor: 'rgba(16, 185, 129, 0.2)',
                        pointBackgroundColor: '#10B981',
                        pointBorderColor: '#10B981',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        borderWidth: 2
                    },
                    {
                        label: 'Left Emp. Rating',
                        data: getAverageRatings(leftEmployees),
                        borderColor: '#EF4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.2)',
                        pointBackgroundColor: '#EF4444',
                        pointBorderColor: '#EF4444',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        borderWidth: 2
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
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 2
                }]
            };
        }
        
        chart.data = data;
        chart.update();
    }
</script>

<div class="bg-white rounded-2xl shadow p-6 h-92">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">
        {showAttrition ? 'Satisfaction Ratings (Attrition Comparison)' : 'Employee Satisfaction Overview'}
    </h3>
    <div class="h-75">
        <canvas bind:this={canvas}></canvas>
    </div>
</div>