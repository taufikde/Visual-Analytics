<script>
async function generateRetentionSuggestions(employeeData, topFeatures) {
    try {
        // Format risk factors for the prompt
        const riskFactorsText = topFeatures.map((factor, idx) => 
            `${idx + 1}. ${factor.feature.replace('cat__', '').replace('num__', '').replace('_', ' ')}: Impact ${factor.impact > 0 ? '+' : ''}${factor.impact.toFixed(3)} (${factor.impact > 0 ? 'Increases' : 'Decreases'} attrition risk)`
        ).join('\n');

        const prompt = `As an HR expert, analyze this employee's attrition risk factors and provide 3 brief, actionable retention suggestions.

        Employee Profile:
        - Age: ${employeeData.Age}
        - Department: ${employeeData.Department}
        - Job Role: ${employeeData.JobRole}
        - Years at Company: ${employeeData.YearsAtCompany}
        - Monthly Income: $${employeeData.MonthlyIncome}
        - Attrition Risk: ${(employeeData.probability * 100).toFixed(1)}%

        Top Risk Factors:
        ${riskFactorsText}

        Provide exactly 3 concise, specific retention strategies (max 15 words each) that directly address these risk factors. Format as:
        1. [suggestion]
        2. [suggestion]
        3. [suggestion]`;
       
        const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-4.1-nano',
                messages: [
                    {
                        role: 'system',
                        content: 'You are an expert HR consultant specializing in employee retention strategies.'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                max_tokens: 200,
                temperature: 0.7
            })
        });

        if (!response.ok) {
            throw new Error(`OpenAI API error: ${response.status}`);
        }

        const data = await response.json();
        const suggestions = data.choices[0].message.content.trim();
        
        // Parse the numbered suggestions into an array
        const suggestionList = suggestions
            .split('\n')
            .filter(line => line.match(/^\d+\./))
            .map(line => line.replace(/^\d+\.\s*/, '').trim());

        return suggestionList;
    } catch (error) {
        console.error('Error generating retention suggestions:', error);
        return [
            'Schedule regular check-ins to discuss career goals',
            'Review compensation and benefits package',
            'Provide professional development opportunities'
        ];
    }
}
  
  export let topEmployees = [];
  export let employees = [];
  export let selectedDept = null;
  
  // Track which employee's risk factors are being shown in modal
  let selectedEmployeeForModal = null;
  
  // Track retention suggestions loading and data
  let loadingSuggestions = {};
  let retentionSuggestions = {};
  
  // Function to show risk factors modal
  function showRiskFactors(employeeIndex) {
    selectedEmployeeForModal = employeeIndex;
  }
  
  // Function to close modal
  function closeModal() {
    selectedEmployeeForModal = null;
  }
  
  // NEW: Function to generate retention suggestions
  async function getRetentionSuggestions(employeeIndex) {
    if (retentionSuggestions[employeeIndex]) {
      // If suggestions already exist, just open the modal
      showRiskFactors(employeeIndex);
      return;
    }
    
    loadingSuggestions[employeeIndex] = true;
    loadingSuggestions = { ...loadingSuggestions }; // Trigger reactivity
    
    try {
      const employee = topEmployees.find(emp => emp.employee_index === employeeIndex);
      const employeeDetails = getEmployeeDetails(employeeIndex);
      
      const suggestions = await generateRetentionSuggestions(
        { ...employeeDetails, probability: employee.probability },
        employee.top_features
      );
      
      retentionSuggestions[employeeIndex] = suggestions;
      retentionSuggestions = { ...retentionSuggestions }; // Trigger reactivity
      
      // Auto-open modal after suggestions are loaded
      showRiskFactors(employeeIndex);
    } catch (error) {
      console.error('Failed to get retention suggestions:', error);
      retentionSuggestions[employeeIndex] = [
        'Schedule regular check-ins to discuss career goals',
        'Review compensation and benefits package',  
        'Provide professional development opportunities'
      ];
      retentionSuggestions = { ...retentionSuggestions };
      
      // Still open modal even if there's an error
      showRiskFactors(employeeIndex);
    } finally {
      loadingSuggestions[employeeIndex] = false;
      loadingSuggestions = { ...loadingSuggestions };
    }
  }
  
  // Filter top employees by department if selected
  $: filteredTopEmployees = selectedDept 
    ? topEmployees.filter(emp => {
        const employeeDetails = getEmployeeDetails(emp.employee_index);
        return employeeDetails.Department === selectedDept;
      })
    : topEmployees;
  
  // Get selected employee data for modal
  $: selectedEmployee = selectedEmployeeForModal 
    ? topEmployees.find(emp => emp.employee_index === selectedEmployeeForModal)
    : null;
  
  // Function to get employee details from the main dataset
  function getEmployeeDetails(employeeIndex) {
    return employees[employeeIndex] || {
      Age: 'N/A',
      Department: 'N/A',
      JobRole: 'N/A',
      YearsAtCompany: 'N/A',
      MonthlyIncome: 'N/A'
    };

  }
  
  // Function to format feature names for display
  function formatFeatureName(featureName) {
    return featureName
      .replace('cat__', '')
      .replace('num__', '')
      .replace('_', ' ')
      .replace(/([A-Z])/g, ' $1')
      .trim();
  }

function extractFeatureKey(featureName) {
  // Remove prefix 'cat__' or 'num__'
  const withoutPrefix = featureName.replace(/^(cat__|num__)/, '');
  
  // Extract the first part before the first underscore
  // If there's no underscore, just return the full string after prefix removal
  const key = withoutPrefix.split('_')[0];
  
  return key;
}
  
  // Function to determine risk level color
  function getRiskColor(probability) {
    if (probability >= 0.9) return 'bg-red-500';
    if (probability >= 0.8) return 'bg-orange-500';
    if (probability >= 0.7) return 'bg-yellow-500';
    return 'bg-green-500';
  }
  
  // Function to get risk level text
  function getRiskLevel(probability) {
    if (probability >= 0.9) return 'Critical';
    if (probability >= 0.8) return 'High';
    if (probability >= 0.7) return 'Medium';
    return 'Low';
  }
  
  // Function to format currency
  function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }
</script>

<!-- At-Risk Employees Section -->
{#if filteredTopEmployees.length > 0}
  <div class="mt-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
        <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        At-Risk Employees
      </h3>
      <span class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full font-medium">
        {filteredTopEmployees.length} employees need attention
      </span>
    </div>
    
    <!-- Enhanced Employee Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {#each filteredTopEmployees as employee}
        {@const employeeDetails = getEmployeeDetails(employee.employee_index)}
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-200 overflow-hidden">
          <!-- Enhanced Card Header -->
          <div class="p-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-md">
                  <span class="text-sm font-bold text-white">#{employee.employee_index}</span>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900 text-sm">Employee #{employee.employee_index}</h4>
                  <p class="text-xs text-gray-600 truncate max-w-24">{employeeDetails.JobRole}</p>
                </div>
              </div>
              <button 
                class="p-2 text-blue-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-all duration-200 transform hover:scale-110"
                on:click={() => showRiskFactors(employee.employee_index)}
                title="View risk factors"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                info
              </button>
            </div>
            
            <!-- Enhanced Risk Level and Probability -->
            <div class="flex items-center justify-between mb-3">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold {getRiskColor(employee.probability)} text-white shadow-sm">
                {getRiskLevel(employee.probability)}
              </span>
              <div class="text-right">
                <span class="text-2xl font-bold text-gray-900">{(employee.probability * 100).toFixed(1)}%</span>
                <p class="text-xs text-gray-500">Risk Score</p>
              </div>
            </div>
            
            <!-- Enhanced Key Info -->
            <div class="bg-gray-50 rounded-lg p-3 mb-3">
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span class="text-gray-600">Age:</span>
                  <span class="font-semibold text-gray-900">{employeeDetails.Age}</span>
                </div>
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span class="text-gray-600">Years:</span>
                  <span class="font-semibold text-gray-900">{employeeDetails.YearsAtCompany}</span>
                </div>
                <div class="col-span-2 flex items-center space-x-1">
                  <div class="w-2 h-2 bg-purple-400 rounded-full"></div>
                  <span class="text-gray-600">Income:</span>
                  <span class="font-semibold text-gray-900">{formatCurrency(employeeDetails.MonthlyIncome)}</span>
                </div>
              </div>
            </div>
            
            <!-- Top Risk Factors Preview (compact) -->
            <div class="mb-3">
              <div class="flex items-center space-x-2 mb-2">
                <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                <h5 class="text-xs font-semibold text-gray-700">Top Risk Factors</h5>
              </div>
              <div class="flex flex-wrap gap-1">
                {#each employee.top_features.slice(0, 3) as feature}
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs {feature.impact > 0 ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}">
                    {formatFeatureName(feature.feature)}
                  </span>
                {/each}
                {#if employee.top_features.length > 3}
                  <button 
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors"
                    on:click={() => showRiskFactors(employee.employee_index)}
                  >
                    +{employee.top_features.length - 3} more
                  </button>
                {/if}
              </div>
            </div>
            
            <!-- UPDATED: Enhanced Action Buttons Section -->
            <div class="flex space-x-2">
              <!-- NEW: Retention Suggestions Button -->
              <button 
                class="w-full bg-gradient-to-r {retentionSuggestions[employee.employee_index] ? 'from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800' : 'from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'} text-white text-xs font-semibold py-2.5 px-3 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-105 flex items-center justify-center space-x-2"
                on:click={() => getRetentionSuggestions(employee.employee_index)}
                disabled={loadingSuggestions[employee.employee_index]}
              >
                {#if loadingSuggestions[employee.employee_index]}
                  <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Generating...</span>
                {:else if retentionSuggestions[employee.employee_index]}
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>View Retention Tips</span>
                {:else}
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  <span>Get Retention Tips</span>
                {/if}
              </button>
              
              <!-- Existing Schedule Meeting Button -->
              <button class="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-xs font-semibold py-2.5 px-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-105">
                Schedule 1:1 Meeting
              </button>
            </div>
            

          </div>
        </div>
      {/each}
    </div>
  </div>
{:else}
  <!-- Enhanced No at-risk employees message -->
  <div class="mt-6 text-center py-12">
    <div class="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
      <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h3 class="text-xl font-semibold text-gray-900 mb-2">No high-risk employees{selectedDept ? ` in ${selectedDept}` : ''}</h3>
    <p class="text-md text-gray-500 max-w-md mx-auto">Great news! No employees are currently at high risk of attrition{selectedDept ? ' in this department' : ''}. Keep up the great work!</p>
  </div>
{/if}

<!-- Risk Factors Modal -->
{#if selectedEmployeeForModal && selectedEmployee}
  {@const employeeDetails = getEmployeeDetails(selectedEmployee.employee_index)}
  <div class="fixed inset-0 bg-opacity-50 flex items-center justify-center z-50 p-4" on:click={closeModal}>
    <div class="bg-white rounded-2xl shadow-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto" on:click|stopPropagation>
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-red-500 to-red-600 text-white p-6 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-16 h-16 bg-white text-red-600 bg-opacity-20 rounded-full flex items-center justify-center">
              <span class="text-lg font-bold">#{selectedEmployee.employee_index}</span>
            </div>
            <div>
              <h3 class="text-xl font-bold">Employee #{selectedEmployee.employee_index}</h3>
              <p class="text-red-100 text-sm">{employeeDetails.JobRole}</p>
            </div>
          </div>
          <button 
            class="text-white hover:text-red-200 transition-colors p-2"
            on:click={closeModal}
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Risk Score Display -->
        <div class="mt-4 flex items-center justify-between">
          <div class="text-3xl font-bold">{(selectedEmployee.probability * 100).toFixed(1)}%
             <p class="text-xs text-white">Attrition Score</p>
          </div>
           
          <div class="text-right">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-white bg-opacity-20 text-gray-900">
              {getRiskLevel(selectedEmployee.probability)} Risk
            </span>
          </div>
        </div>
      </div>
      
      <!-- Modal Content -->
      <div class="p-6">
        <!-- Employee Details -->
        <div class="bg-gray-50 rounded-lg p-4 mb-6">
          <h4 class="font-semibold text-gray-900 mb-3">Employee Details</h4>
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-blue-400 rounded-full"></div>
              <span class="text-gray-600">Age:</span>
              <span class="font-semibold text-gray-900">{employeeDetails.Age}</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-green-400 rounded-full"></div>
              <span class="text-gray-600">Years:</span>
              <span class="font-semibold text-gray-900">{employeeDetails.YearsAtCompany}</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-purple-400 rounded-full"></div>
              <span class="text-gray-600">Department:</span>
              <span class="font-semibold text-gray-900">{employeeDetails.Department}</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <span class="text-gray-600">Income:</span>
              <span class="font-semibold text-gray-900">{formatCurrency(employeeDetails.MonthlyIncome)}</span>
            </div>
          </div>
        </div>
        
        <!-- Risk Factors -->
        <div class="mb-6">
          <h4 class="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <span>Risk Factors Analysis</span>
          </h4>
          <div class="space-y-3">
            {#each selectedEmployee.top_features as feature, idx}
              <div class="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors">
                <div class="flex items-center space-x-3">
                  <div class="flex-shrink-0 w-6 h-6 rounded-full {feature.impact > 0 ? 'bg-red-100' : 'bg-blue-100'} flex items-center justify-center">
                    <span class="text-xs font-bold {feature.impact > 0 ? 'text-red-600' : 'text-blue-600'}">
                      {idx + 1}
                    </span>
                  </div>
                  <div>
                    <span class="font-medium text-gray-900 text-sm">{formatFeatureName(feature.feature)}</span>
                    <p class="font-medium text-gray-500 text-sm">{employeeDetails[extractFeatureKey(feature.feature)]}</p>
                  </div>
                </div>
                <span class="text-sm {feature.impact > 0 ? 'text-red-600 bg-red-50' : 'text-blue-600 bg-blue-50'} font-mono px-3 py-1 rounded-full">
                  {feature.impact > 0 ? '+' : ''}{(feature.impact * 100).toFixed(2)}
                </span>
              </div>
            {/each}
          </div>
        </div>
        
        <!-- NEW: Retention Suggestions in Modal -->
        {#if retentionSuggestions[selectedEmployee.employee_index]}
          <div class="mb-6 bg-green-50 rounded-lg p-4 border border-green-200">
            <h4 class="font-semibold text-green-800 mb-3 flex items-center space-x-2">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>Personalized Retention Strategies</span>
            </h4>
            <div class="space-y-2">
              {#each retentionSuggestions[selectedEmployee.employee_index] as suggestion, idx}
                <div class="flex items-start space-x-3 p-2 bg-white rounded-lg">
                  <div class="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                    <span class="text-xs font-bold text-green-600">{idx + 1}</span>
                  </div>
                  <span class="text-sm text-green-700 font-medium">{suggestion}</span>
                </div>
              {/each}
            </div>
          </div>
        {/if}
        
        <!-- Action Buttons -->
        <div class="flex space-x-3">
          <button class="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-sm font-semibold py-3 px-4 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm hover:shadow-md">
            Schedule 1:1 Meeting
          </button>
          <button class="flex-1 bg-gray-100 text-gray-700 text-sm font-semibold py-3 px-4 rounded-lg hover:bg-gray-200 transition-colors">
            View Full Profile
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Custom animations for smooth transitions */
  .transition-all {
    transition: all 0.2s ease-in-out;
  }
  
  /* Modal backdrop blur effect */
  .fixed {
    backdrop-filter: blur(4px);
  }
</style>