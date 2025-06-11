<script>
  export let role;
  export let count = 0;
</script>

<div class="flex-shrink-0 w-40 h-32 border border-gray-300 rounded-lg p-4 flex flex-col items-center justify-center bg-white hover:shadow transition-shadow duration-200">
  <span class="text-center text-gray-800 font-semibold text-sm leading-tight">{role}</span>

  <span class="mt-2 text-blue-600 text-2xl font-bold">
    {count}
  </span>

  <span class="text-gray-500 text-sm">
    {count === 1 ? 'employee' : 'employees'}
  </span>
</div>
