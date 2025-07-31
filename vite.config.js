import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '')
	return {
		plugins: [tailwindcss(), sveltekit()],
		define: {
		__APP_ENV__: JSON.stringify(env.APP_ENV),
		},
	}
});
