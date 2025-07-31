<script>
  export let role;
  export let count = 0;
</script>

<div class="w-44 h-28 bg-white rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 p-4 flex flex-col justify-center items-center">
  <div class="text-3xl font-bold text-blue-600 mt-2 leading-snug">
    {count}
  </div>
    <div class="text-sm text-gray-600 font-medium text-center leading-tight">
    {role}
  </div>
</div>
