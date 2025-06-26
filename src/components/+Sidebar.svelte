<script>
  import { createEventDispatcher } from 'svelte';
  import { Home, Users, Table  } from '@lucide/svelte';

  // Sidebar items (no types—plain JS)
  const items = [
    { key: 'dashboard', label: 'Dashboard', Icon: Home },
    { key: 'department', label: 'Department', Icon: Users },
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

<aside class="flex flex-col bg-gradient-to-b from-blue-800 to-blue-700 text-white w-64 h-screen p-4">
  <div class="mb-8">
    <h1 class="text-2xl font-bold">HR Analytics</h1>
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
            <svelte:component this="{item.Icon}" class="w-5 h-5" />
            <span class="font-medium">{item.label}</span>
        </button>
        {/each}
  </nav>

  <footer class="mt-auto text-sm text-blue-200">
    <p>© 2025 </p>
  </footer>
</aside>
