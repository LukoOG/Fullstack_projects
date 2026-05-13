<script lang="ts">
    import { page } from "$app/state";
    import { goto } from "$app/navigation";
    import { enhance } from '$app/forms';
    import type { PageProps } from "./$types.js";
	import { X, ArrowLeft } from "@lucide/svelte";
	
	import Button from "$lib/components/ui/button.svelte";
    import Login from "$lib/components/auth/login.svelte";
    import Register from "$lib/components/auth/register.svelte";
	
	type FormState = "login" | "register"

    let { form }: PageProps = $props()
	
	let isLogin = $state<boolean>(true)
	let formAction: FormState = $derived.by(()=>isLogin ? "login" : "register")
	let disableSubmitBtn = $state<boolean>(false)
	
	const handleEnhance = () => {
		disableSubmitBtn = true
		
		return async ({ update }) => {
			await update()
			disableSubmitBtn = false
		}
	}
	

	function goBack() {
		history.length > 1 ? history.back() : goto("/");
	}

	function setIsLogin(value: boolean){
		isLogin = value
	}
	
</script>

<!-- snippetss -->
{#snippet changeFormBtn(form: String | null)}
    <p class="text-sm text-gray-600 text-center">
        {#if form == "login"}
            Don’t have an account? <a href={undefined} onclick={()=>updateAuthSearchParams("register")} class="text-orange-500 cursor-pointer hover:underline">Register</a>
        {:else if form == "register"}
            Already have an account? <a href={undefined} onclick={()=>updateAuthSearchParams("login")} class="text-orange-500 cursor-pointer hover:underline">Login</a>
        {/if}
    </p>
{/snippet}

<!-- main html body -->
<div class="min-h-screen w-full flex items-center justify-center bg-background px-4">
	<div class="w-full max-w-md space-y-8">
		<!-- Back button -->
		<Button
			onclick={goBack}
			class="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-4"
			variant="ghost"
			size="sm"
		>
			<ArrowLeft class="h-5 w-5" />
			<span class="text-sm font-medium">Back</span>
		</Button>
		<!-- Header -->
		<div class="text-center">
			<h1 class="text-3xl font-bold text-foreground">Swix</h1>
			<p class="mt-2 text-muted-foreground">
				{isLogin ? "Welcome back" : "Join the conversation"}
			</p>
		</div>

		<!-- Form Container -->
		<div class="bg-card border border-border rounded-lg p-6 shadow-sm">
			<!-- Toggle Buttons -->
			<div class="flex mb-6 p-1 bg-muted rounded-lg">
				<Button variant={isLogin ? "default" : "ghost"} class="flex-1 cursor-pointer" onclick={() => {isLogin = true}}>
					Sign In
				</Button>
				<Button variant={!isLogin ? "default" : "ghost"} class="flex-1 cursor-pointer" onclick={() => {isLogin = false}}>
					Sign Up
				</Button>
			</div>

			<!-- Forms -->
			<form method="POST" class="space-y-4" action="?/{formAction}" use:enhance={handleEnhance}>
				{#if isLogin}
					<Login disable={disableSubmitBtn} />
				{:else if !isLogin}
					<Register disable={disableSubmitBtn} />
				{/if}
			</form>
			
		</div>

		<!-- Footer -->
		<div class="text-center text-sm text-muted-foreground">
			<p>{isLogin ? "Don't have an account? " : "Already have an account? "}
				<button onclick={() => setIsLogin(!isLogin)} class="text-primary hover:underline font-medium">
					{isLogin ? "Sign up" : "Sign in"}
				</button>
			</p>
		</div>
	</div>
	{#if form?.error}
		<div class="p-4 rounded-md border border-border absolute right-1 top-[-25%] bg-destructive h-fit min-w-full">
			<p class="text-md font-semibold text-center text-destructive-foreground">{ form.error.detail }</p>
		</div>
	{/if}
</div>

