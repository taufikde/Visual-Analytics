<script>
  import { createEventDispatcher } from 'svelte';
  import { Home, Users, Table, LayoutDashboard  } from '@lucide/svelte';

  // Sidebar items (no types—plain JS)
  const items = [
    { key: 'dashboard', label: 'Dashboard', Icon: Home },
    { key: 'datagrid', label: 'DataGrid', Icon: Table }
  ];

  // The currently selected key; default to "dashboard"
  export let selected = 'dashboard';

  const dispatch = createEventDispatcher();

  function handleClick(key) {
    if (key !== selected) {
      dispatch('select', key);
    }
  }
</script>

<aside class="flex flex-col bg-gradient-to-b from-blue-800 to-blue-700 text-white w-24 h-screen p-4">
  <div class="mb-8 ml-3">
    <LayoutDashboard class="w-8 h-8" /> 
  </div>

  <nav class="flex-1">
        {#each items as item}
        <button
            on:click="{() => handleClick(item.key)}"
            class="w-full flex items-center space-x-3 px-4 py-2 mb-2 rounded-lg transition-colors duration-200
                {selected === item.key
                    ? 'bg-white text-blue-800 hover:bg-white/90'
                    : 'bg-blue-700/20 hover:bg-blue-700/50'}"
        >
            <svelte:component this="{item.Icon}" class="w-8 h-8" />
           <!-- <span class="font-medium">{item.label}</span> -->
        </button>
        {/each}
  </nav>

  <footer class="mt-auto text-sm text-blue-200">
    <p class="text-center"> Taufik Tamboli © 2025 </p>
  </footer>
</aside>
