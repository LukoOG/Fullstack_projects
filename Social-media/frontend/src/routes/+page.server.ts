import { BACKEND_URL } from "$env/static/private"

export const load = async ({ cookies, fetch }) => {
	const access = cookies.get("accessToken");
	const res = await fetch(`${BACKEND_URL}/api/posts/feed`, {
		headers:{
			"Access-Control-Allow-Origin":"127.0.0.1:8000",
			"Authorization": access ? `Bearer ${access}` : "",
			
		}
	})
	
	if (res.ok){
		const data = await res.json()
		console.log(data)
		return {
			posts: data.results,
			next: data.next,
			previous: data.previous,
		}
	}
}