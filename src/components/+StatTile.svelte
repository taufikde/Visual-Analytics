<script>
  export let value;
  export let label;
</script>

<div class="w-44 h-32 bg-white rounded-2xl mt-2 mx-2 shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 p-4 flex flex-col justify-center items-center">
  <div class="text-4xl font-bold text-blue-600 mt-2 leading-snug">
    {value}
  </div>
  <div class="text-sm text-gray-500 font-medium mt-1 text-center">
    {label}
  </div>
</div>
