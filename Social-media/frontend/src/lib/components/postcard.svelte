<script lang="ts">
	import { DropdownMenu } from "bits-ui";
	import { MoreHorizontal, MessageCircle, Repeat2, Heart, Share } from "@lucide/svelte";
	import { formatDistanceToNow } from "date-fns";
	import Button from "$lib/components/ui/button.svelte";
	
	import { enhance } from "$app/forms";
	
	let { post } = $props()
	let isLiked = $state<boolean>(post.is_liked)
	let likesCount = $state<number>(post.likes_count)
	
	//$inspect(isLiked)
	
	const handleReply = () => {}
	const handleLike = () => {}
	const handleComment = () => {}
	const handleRepost = () => {}
	
	
	const handleLikeEnhance = async () => {
		return async ({ result, update }) => {
			await update();

			const { liked, likes } = result
			isLiked = liked ?? is_liked
			likesCount = likes ?? likes_count
		}
	}
</script>

<div class="rounded-lg border bg-card text-card-foreground shadow-sm border-0 border-b rounded-none transition-colors hover:bg-muted/20">
	<div class="p-4 p-6 pt-0">
		<div class="flex space-x-3">
			<div class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full h-12 w-12">
				{#if post.author.avatar}
					<img class="aspect-square h-full w-full" src={post.author.avatar} alt={post.author} />
				{:else}
					<div class="flex h-full w-full items-center justify-center rounded-full bg-muted">{post.author.name[0]}</div>
				{/if}
			</div>
		  
			<div class="flex-1 min-w-0">
				<div class="flex items-center space-x-2">
					<h3 class="font-bold text-foreground hover:underline cursor-pointer">
						<a class="contents" href="/profile/{post.author.username}">{post.author.name}</a>
					</h3>

					<span class="text-muted-foreground">@{post.author.username}</span>
					<span class="text-muted-foreground">·</span>
					<span class="text-muted-foreground text-sm">
						{formatDistanceToNow(post.created_at, { addSuffix: true })}
					</span>
									  

					<div class="ml-auto">
					  <DropdownMenu.Root>
						<DropdownMenu.Trigger>
						  <Button variant="ghost" size="icon" class="h-8 w-8">
							<MoreHorizontal class="h-4 w-4" />
						  </Button>
						</DropdownMenu.Trigger>

						<DropdownMenu.Content align="end" class="z-50 min-w-[8rem] rounded-md border bg-popover p-3 shadow-md">
						  <DropdownMenu.Item class="rounded-button data-highlighted:bg-muted ring-0! ring-transparent! flex h-10 select-none items-center py-3 pl-3 pr-1.5 text-sm font-medium focus-visible:outline-none">
							Follow @{post.author.username}
						  </DropdownMenu.Item>
						  <DropdownMenu.Item class="rounded-button data-highlighted:bg-muted ring-0! ring-transparent! flex h-10 select-none items-center py-3 pl-3 pr-1.5 text-sm font-medium focus-visible:outline-none">
							Mute @{post.author.username}
						  </DropdownMenu.Item>
						  <DropdownMenu.Item class="rounded-button data-highlighted:bg-muted ring-0! ring-transparent! flex h-10 select-none items-center py-3 pl-3 pr-1.5 text-sm font-medium focus-visible:outline-none">
							Block @{post.author.username}
						  </DropdownMenu.Item>
						</DropdownMenu.Content>
					  </DropdownMenu.Root>
					</div>
					
				</div>

				<div class="mt-2 space-y-3">
				  <p class="text-foreground whitespace-pre-wrap break-words leading-relaxed">{post.content}</p>
				  
				  {#if post.image}
					<div class="rounded-2xl overflow-hidden border border-border">
					  <img src={post.image} 
						alt="Post content" 
						class="w-full h-auto object-cover transition-transform duration-200 hover:scale-[1.02]"
					  />
					</div>
				  {/if}
				</div>

				<div class="flex items-center justify-between mt-4 max-w-md">
					<Button variant="ghost" size="sm" class="text-muted-foreground hover:text-social-blue hover:bg-social-blue/10 transition-all duration-200">
						<MessageCircle class="h-4 w-4 mr-1" />
						<span class="text-sm">{post.repliesCount}</span>
					</Button>

					<Button variant={post.isReposted ? "repost-active" : "repost"} size="sm">
						<Repeat2 class="h-4 w-4 mr-1" />
						<span class="text-sm">{post.repostsCount}</span>
					</Button>
					
					<form method="POST" action={`/api/posts/${post.id}/like`} use:enhance={handleLikeEnhance}>
						<Button type="submit" variant={isLiked ? "like-active" : "like"} size="sm">
							<Heart class={`h-4 w-4 mr-1 ${isLiked ? 'fill-current' : ''}`} />
							<span class="text-sm">{likesCount}</span>
						</Button>
					</form>

					<Button variant="ghost" size="sm" class="text-muted-foreground hover:text-social-blue hover:bg-social-blue/10 transition-all duration-200">
						<Share class="h-4 w-4" />
					</Button>
				</div>
				
			</div>
		</div>
	</div>
</div>