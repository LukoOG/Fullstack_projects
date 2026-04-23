<script lang="ts">
	import { Calendar, MapPin, Smile, ImageIcon, X } from '@lucide/svelte';
	import Button from '$lib/components/ui/button.svelte';
	import Textarea from '$lib/components/ui/textarea.svelte';
	import Input from '$lib/components/ui/input.svelte';

	import { enhance } from '$app/forms';

	import { Avatar } from 'bits-ui';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let { user, addPost } = $props();

	let fileInput = $state();
	let file = $state();
	//let newPost = $state(null)

	const maxChars = 100;
	let content = $state<string>('');
	const remainingChars = $derived(maxChars - content.length);
	let isOverLimit = $derived(remainingChars < 0);
	let isNearLimit = $derived(remainingChars <= 20);
	let progress = $derived(Math.min((content.length / maxChars) * 100, 100));

	function handleEnhance() {
		return async ({ update, result }) => {
			await update();
			addPost(result);

			//clear values
			content = '';
			file = null;
			removeImage();
		};
	}

	let imagePreview = $state<string | null>(null);

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];

		// Revoke previous URL to avoid memory leaks
		if (imagePreview) {
			URL.revokeObjectURL(imagePreview);
		}

		if (file) {
			imagePreview = URL.createObjectURL(file);
		} else {
			imagePreview = null;
		}
	}

	function removeImage() {
		if (imagePreview) {
			URL.revokeObjectURL(imagePreview);
			imagePreview = null;
		}
		// Clear the file input so the same file can be re-selected if needed
		if (fileInput) {
			fileInput.value = '';
		}
	}
</script>

<section
	class="rounded-lg rounded-none border border-0 border-b bg-card text-card-foreground shadow-sm"
>
	<div class="p-6">
		<div class="flex space-x-3">
			<Avatar.Root class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
				<Avatar.Image class="aspect-square h-full w-full" src={user.avatar} />
				<Avatar.Fallback
					class="flex aspect-square h-12 w-12 items-center justify-center rounded-full bg-muted"
					>{'asad'.toUpperCase()}</Avatar.Fallback
				>
			</Avatar.Root>

			<div class="flex-1 space-y-4">
				<Textarea
					placeholder="What's happening?"
					bind:value={content}
					class="min-h-[60px] resize-none border-0 p-0 text-xl placeholder:text-muted-foreground focus-visible:ring-0"
					style="box-shadow: none;"
				/>

				<!-- Image Preview -->
				{#if imagePreview}
					<div class="relative overflow-hidden rounded-xl border">
						<img src={imagePreview} alt="Upload preview" class="max-h-80 w-full object-cover" />
						<button
							onclick={removeImage}
							class="absolute top-2 right-2 rounded-full bg-black/60 p-1 text-white transition-colors hover:bg-black/80"
							aria-label="Remove image"
						>
							<X class="h-4 w-4" />
						</button>
					</div>
				{/if}

				<div class="flex items-center justify-between">
					<div class="flex items-center space-x-4">
						<form
							id="postForm"
							method="POST"
							action="/api/posts"
							enctype="multipart/form-data"
							use:enhance={handleEnhance}
						>
							<Button
								onclick={() => fileInput.click()}
								variant="ghost"
								size="icon"
								class="h-9 w-9 text-social-blue hover:bg-social-blue/10"
							>
								<ImageIcon class="h-5 w-5" />
								<input
									bind:this={fileInput}
									name="media"
									class="hidden"
									type="file"
									onchange={handleFileChange}
								/>
								<input bind:value={content} name="content" class="hidden" type="text" />
							</Button>
						</form>

						<Button
							variant="ghost"
							size="icon"
							class="h-9 w-9 text-social-blue hover:bg-social-blue/10"
						>
							<MapPin class="h-5 w-5" />
						</Button>
						<Button
							variant="ghost"
							size="icon"
							class="h-9 w-9 text-social-blue hover:bg-social-blue/10"
						>
							<Smile class="h-5 w-5" />
						</Button>
						<Button
							variant="ghost"
							size="icon"
							class="h-9 w-9 text-social-blue hover:bg-social-blue/10"
						>
							<Calendar class="h-5 w-5" />
						</Button>
					</div>

					<div class="flex items-center space-x-3">
						{#if true}
							<div class="flex items-center space-x-2">
								<div class="relative h-8 w-8">
									<svg class="h-8 w-8 -rotate-90 transform" viewBox="0 0 36 36">
										<!-- Background circle -->
										<path
											class="stroke-current text-muted-foreground/20"
											stroke-width="4"
											fill="none"
											d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
										/>
										<!-- Progress circle -->
										<path
											class="stroke-current"
											class:text-destructive={isOverLimit}
											class:text-yellow-500={isNearLimit && !isOverLimit}
											class:text-social-blue={!isNearLimit && !isOverLimit}
											stroke-width="4"
											fill="none"
											stroke-dasharray="{progress}, 100"
											d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
										/>
									</svg>
								</div>
								{#if isNearLimit}
									<span class="text-sm {isOverLimit ? 'text-destructive' : 'text-yellow-600'}">
										{remainingChars}
									</span>
								{/if}
							</div>
						{/if}

						<Button
							variant="social"
							size="sm"
							disabled={!content.trim() || isOverLimit}
							class="px-6"
							type="submit"
							form="postForm"
						>
							Post
						</Button>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>
