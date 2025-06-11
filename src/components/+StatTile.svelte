<script>
  export let value;
  export let label;
</script>

<div class="flex-shrink-0 w-52 border border-gray-300 rounded-lg p-6 bg-white hover:shadow transition-shadow duration-200">
  <div class="text-center">
    <span class="block text-3xl font-bold text-blue-600">{value}</span>
    <span class="mt-2 text-gray-600 font-medium">{label}</span>
  </div>
</div>