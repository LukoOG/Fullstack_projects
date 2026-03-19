<script lang="ts">
	import Postcard from "$lib/components/postcard.svelte";
	import { enhance } from "$app/forms";
	import { Avatar, Tabs } from "bits-ui";
	import { MapPin, LinkIcon, Calendar, Users, Settings } from "@lucide/svelte";
	import Button from "$lib/components/ui/button.svelte";
	import { goto, invalidate } from "$app/navigation";
	import { page } from "$app/state";
	
	const handleFollow = () => {}
	
	let { data } = $props()
	let { posts = [], userData, followers = [], user } = $derived(data)
	let isFollowing = $derived(followers ? followers.some((follower)=>follower.username === user.username) : false);
	$inspect(followers)
	
	let username = $derived(page.params.username)
	
	function handleProfileClick(username) {
		goto(`/profile/${username}`, { invalidateAll: true });
	}
	
	let followerCount = $derived<number>(userData.followers)
	
	const handleFollowEnhance = async () => {
		return async ({ result, update }) => {
			await update();
			const { following, no_follows } = result.data
			console.log(no_follows)
			isFollowing = following
			followerCount = no_follows
		}
	}
</script>

{#snippet FollowOrEdit()}
	{#if !user}
		
	{:else if user.username === username}
		<Settings class="cursor-pointer" size={24} onclick={ () => goto("/profile/edit") } />
	{:else if user.username !== username}
		<form method="POST" action="?/toggle_follow" use:enhance={handleFollowEnhance}>
			<Button type="submit" variant= {isFollowing ? "outline" : "social"} onClick={handleFollow} class="px-6">
				{isFollowing ? "Unfollow" : "Follow"}
			</Button>
		</form>
	{/if}
{/snippet}

<section class="p-2 max-w-2xl ml-4">
      <!-- Header -->
      <div class="sticky top-0 z-10 bg-background/95 backdrop-blur border-b p-4">
        <div>
          <h1 class="text-xl font-bold">{userData.name}</h1>
          <p class="text-sm text-muted-foreground">{userData.posts} {userData.posts > 1 ? "posts" : "post"} </p>
        </div>
      </div>

      <!-- Profile Header -->
      <div class="p-6 border-b">
        <div class="flex items-start justify-between mb-4">
          <Avatar.Root class="h-24 w-24">
            <Avatar.Image class="aspect-square h-full w-full" src={userData.profile_pic} />
            <Avatar.Fallback class="flex h-full w-full items-center justify-center rounded-full bg-muted aspect-square text-2xl">{userData.name[0]}</Avatar.Fallback>
          </Avatar.Root>
		  
		  {@render FollowOrEdit()}
        </div>

        <div class="space-y-3">
          <div>
            <h1 class="text-2xl font-bold">{userData.name}</h1>
            <p class="text-muted-foreground">@{userData.username}</p>
          </div>

          <p class="text-foreground">{userData.bio}</p>

          <div class="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
            <div class="flex items-center gap-1">
              <MapPin class="h-4 w-4" />
              <span>{userData.location}</span>
            </div>
            <div class="flex items-center gap-1">
              <LinkIcon class="h-4 w-4" />
              <a target="blank" href={userData.website} class="text-social-blue hover:underline">
                {userData.website}
              </a>
            </div>
            <div class="flex items-center gap-1">
              <Calendar class="h-4 w-4" />
              <span>Joined {userData.joinedDate}</span>
            </div>
          </div>

          <div class="flex items-center gap-6 text-sm">
            <div>
              <span class="font-bold text-foreground">{userData.following}</span>
              <span class="text-muted-foreground ml-1">Following</span>
            </div>
            <div>
              <span class="font-bold text-foreground">{followerCount}</span>
              <span class="text-muted-foreground ml-1">{userData.followers > 1 ? "Followers" : "Follower"}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <Tabs.Root value="posts" class="w-full">
        <Tabs.List class="grid w-full grid-cols-3 bg-transparent border-b rounded-none h-auto">
          <Tabs.Trigger value="posts" class="data-[state=active]:border-b-2 cursor-pointer data-[state=active]:border-social-blue rounded-none inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50">
            Posts
          </Tabs.Trigger>
          <Tabs.Trigger value="replies" class="data-[state=active]:border-b-2 cursor-pointer data-[state=active]:border-social-blue rounded-none inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50">
            Replies
          </Tabs.Trigger>
          <Tabs.Trigger value="followers" class="data-[state=active]:border-b-2 cursor-pointer data-[state=active]:border-social-blue rounded-none inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50">
            Followers
          </Tabs.Trigger>
        </Tabs.List>
        
        <Tabs.Content value="posts" class="mt-0">
			<div class="divide-y divide-border">
				{#each posts as post (post.id)}
					<Postcard {post} />
				{/each}
			</div>
        </Tabs.Content>
        
        <Tabs.Content value="replies" class="mt-0">
          <div class="p-8 text-center text-muted-foreground">
            Replies coming soon!
          </div>
        </Tabs.Content>
        
        <Tabs.Content value="followers" class="mt-0">
          <div class="p-8 text-center text-muted-foreground divide-y">
			{#each followers as follower (follower.id)}
				<div class="rounded-lg border bg-card text-card-foreground shadow-sm border-0 border-b rounded-none cursor-pointer hover:bg-muted/50 transition-colors"
				onclick={()=>handleProfileClick(follower.username)}>
					<div class="p-6 pt-0 p-4">
						<div class="flex items-start justify-between">
							<div class="flex items-start gap-3 flex-1">
								<Avatar.Root class="h-12 w-12">
									<Avatar.Image src={follower.profile_pic} />
									<Avatar.Fallback class="flex h-full w-full items-center justify-center rounded-full bg-muted aspect-square text-2xl">{follower.name[0]}</Avatar.Fallback>
								</Avatar.Root>

								<div class="flex-1 min-w-0">
									<div class="flex items-center gap-2">
										<h3 class="font-semibold text-foreground truncate">
										{follower.name}
										</h3>
										<span class="text-muted-foreground">@{follower.username}</span>
										</div>

										<p class="text-sm text-foreground mt-1 line-clamp-2">
										{follower.bio}
										</p>

										<div class="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
										<div class="flex items-center gap-1">
										<MapPin class="h-3 w-3" />
										<span>{follower.location}</span>
										</div>
										<div class="flex items-center gap-1">
										<Users class="h-3 w-3" />
										<span>{follower.followers} followers</span>
										</div>
									</div>
								</div>
							</div>

							<Button variant="outline" size="sm" class="ml-4">
							View
							</Button>
						</div>
					</div>
				</div>
			{/each}
          </div>
        </Tabs.Content>
      </Tabs.Root>
</section>