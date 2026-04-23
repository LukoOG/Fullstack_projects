<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.png';
	import Sidebar from '$lib/components/sidebar.svelte';
	import { page } from '$app/state';

	let { data, children } = $props();
		
	let route = $derived(page.url.pathname)
	
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Swix</title>
</svelte:head>

<div class="min-h-screen flex w-full">
	{#if route !== "/auth"}
		<Sidebar user={data.user} />
		<div class="flex-1">
			<div class="flex-1">
				<header class="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
					<div class="container flex h-14 items-center">
						<!-- <SidebarTrigger class="md:hidden" /> -->
							<div class="flex flex-1 items-center justify-between space-x-2 md:justify-end">
								<div class="w-full flex-1 md:w-auto md:flex-none">
								<h1 class="text-lg font-semibold md:hidden">SocialApp</h1>
							</div>
						</div>
					</div>
				</header>
			
				<main class="flex-1">
					{@render children?.()}
				</main>
				
			</div>
		</div>
	{:else if route === "/auth"}
		{@render children?.()}
	{/if}
</div>



