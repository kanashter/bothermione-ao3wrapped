<script>
	let loaded = false;
	let u;
	let p;

	async function getWrapped(u, p) {
		let url = `http://127.0.0.1:5001/?username=${u}&password=${p}`;
		let request = await fetch(url, {
			method: 'get'
		});
		let d = await request.json();
		return d;
	}

	function randomEmoji() {
		let array = ['🥵', '💦', '🍆', '🥺', '🍌', '🍑', '😉', '🤤', '👅', '👀', '😳', '💆'];

		return array[Math.floor(Math.random() * array.length)];
	}

	function commaNum(num) {
		return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	}

	function randomString() {
		let array = [
			'Must be a great read',
			'Might have to look into that myself',
			'Do you need help? I think you might need help',
			'Reading is for nerds',
			"Having fun isn't hard when you've got an AO3 account",
			"'Books written by fans are the best books' - William Shakespeare",
			"'Only Big Brain Winners read fanfic' - Albert Einstien",
			"'Yes we can, we can read fanfic' - Barack Obama",
			"'I have a dream, that one day Childhood friends and Enemies to lovers can sit at the same table for romance' - Martin Luther Kink Jr.",
			'These are you 95 Thesis nailed to the door of the internet',
			'get busy readin or get busy dyin',
			"you're here to eat ass and read fanfic, and your all out of fanfic",
			'Make sure you left a comment telling the author how much you love it!'
		];
		return array[Math.floor(Math.random() * array.length)];
	}
</script>

<svelte:head>
	<title>BotHermione - WRAPPED</title>
</svelte:head>

<div class="wrapper">
	<h1>WRAPPED</h1>
	<img src="https://www.bothermione.com/images/logo.jpg" alt="BotHermione">
	<div class="container">
		<p>Look mum I'm a real developer now edition</p>
		<p>
			Hello and welcome to AO3 wrapped. I'm sorry this asks for your password, but AO3 locks a
			readers history beind their account. Smart - but annoying for making these. The version of AO3 wrapped you're using is the local copy, which performs the following actions:
		</p>
		<ul>
			<li>Upon open, spawns a local server to scape data</li>
			<li>Log into your account</li>
			<li>Loop through your history</li>
			<li>Parse data</li>
		</ul>
		<p>
			And thats it. None of your details are stored in this application, nor are they on the server
			performing this operation. I have enough trouble managing my own account - let alone other
			users!
		</p>
		<p>Found this useful? Feel free to <a href="https://twitter.com/bothermione">let me know</a></p>
		<p>
			But, if you're feeling brave - please log in below and see all the grimy details about your
			2021 on AO3
		</p>
	</div>
	{#if loaded == true}
		<div class="container">
			{#await getWrapped(u, p)}
				<p>Loading</p>
			{:then data}
				<div class="wrapped">
					<div class="wrapped-1">
						<h1>{data.username}, this year you read</h1>
						<h2>
							{commaNum(data.total_fics)} fics, and you visited them {commaNum(data.total_reads)} times
						</h2>
						{#if data.total_words > 1000000}
							<h2>That's {commaNum(data.total_words)} words worth of literature! Jesus.</h2>
						{:else}
							<h2>
								That's only {commaNum(data.total_words)} words worth of literature. Get those numbers
								up babes.
							</h2>
						{/if}
					</div>
					<div class="wrapped-2">
						<h3>
							There was one fic you read more than any other. <br /><br />
						</h3>
						<h1>
							❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️<br />
							<i>{data.most_visited.title}</i><br />
							by
							<i>{data.most_visited.author}</i>
							<br />
							❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️
						</h1>
						.
						<h3>
							<br />You went back to it {data.most_visited.count}
							times.
							<br />
							{randomString()}
						</h3>
					</div>
					<div class="wrapped-3">
						<div class="left">
							<h3>
								There were some characters who appeared more than anyone else in what you read.
							</h3>
						</div>
						<div class="right">
							{#each data.most_visited.characters as char, i}
								<p><span class="size-{i + 1}">{i + 1} - {char} {randomEmoji()}</span></p>
							{/each}
						</div>
					</div>
					<div class="wrapped-4">
						<div class="left-alt">
							{#each data.most_visited.relations as rela, i}
								{#if rela == 'NONE'}
									<p>
										<span class="size-{i + 1}"
											>{i + 1} - {randomEmoji()} Nobody! There was no relationship in this fic!</span
										>
									</p>
								{:else}
									<p><span class="size-{i + 1}">{i + 1} - {randomEmoji()} {rela}</span></p>
								{/if}
							{/each}
						</div>
						<div class="right-alt">
							<h3>There were some relationships you liked more than others</h3>
						</div>
					</div>
					<div class="wrapped-5">
						<div class="left">
							<h3>And the fics you read had some pretty consistent themes...</h3>
						</div>
						<div class="right">
							{#each data.most_visited.tags as tag, i}
								<p><span class="size-{i + 1}">{i + 1} - {tag} {randomEmoji()}</span></p>
							{/each}
						</div>
					</div>
				</div>
			{:catch}
				<div class="container login">
					<h1>
						Looks like there was a server error! If you're positive you got your password right,
						please try again later!
					</h1>
					<button on:click={() => (loaded = false)}> Show me the dirt </button>
				</div>
			{/await}
		</div>
	{:else}
		<div class="container login">
			<input bind:value={u} placeholder="username" />
			<input bind:value={p} placeholder="password" type="password" />
			<button on:click={() => (loaded = true)}> Show me the dirt </button>
		</div>
	{/if}
</div>

<style>
	h1 {
		font-size: 3rem;
		font-family: var(--serif-font);
		font-style: italic;
	}
	.wrapper {
		display: flex;
		flex-direction: column;
		width: 100%;
		align-items: center;
		font-family: var(--sans-font);
		font-size: 1.2rem;
	}
	.container {
		width: 60%;
	}
	img {
		width: 200px;
		border-radius: 200px;
	}
	input {
		width: 80%;
		margin-bottom: 2rem;
		background-color: rgba(0, 0, 0, 0);
		color: white;
		font-size: 2rem;
		font-family: var(--serif-font);
		border: 0px solid white;
		border-bottom: 1px solid white;
		text-align: center;
	}
	input:focus {
		outline: none;
		border-bottom: 1px solid aqua;
	}
	.login {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	button {
		width: 80%;
		font-family: var(--sans-font);
		font-size: 1.2rem;
		border: 0px solid rgba(0, 0, 0, 0);
		border-bottom: 2px solid white;
		background-color: rgba(0, 0, 0, 0);
		color: white;
	}
	button:hover {
		background-color: white;
		color: rgba(22, 22, 22);
	}
	.wrapped {
		display: flex;
		flex-direction: column;
	}
	.wrapped-1 {
		background-color: rgb(58, 177, 177);
		padding: 30px;
		text-align: center;
		margin-bottom: 3rem;
	}
	.wrapped-2 {
		background-color: rgb(98, 173, 148);
		padding: 30px;
		text-align: center;
		margin-bottom: 3rem;
	}
	.wrapped-3 {
		background-color: brown;
		padding: 30px;
		display: flex;
		margin-bottom: 3rem;
		position: relative;
	}
	.wrapped-4 {
		background-color: rgb(202, 108, 166);
		padding: 30px;
		display: flex;
		margin-bottom: 3rem;
		position: relative;
	}
	.wrapped-5 {
		background-color: rgb(126, 182, 100);
		padding: 30px;
		display: flex;
		margin-bottom: 3rem;
		position: relative;
	}
	.left {
		position: absolute;
		top: 0;
		bottom: 0;
		display: flex;
		width: 40%;
		align-items: center;
	}
	.right {
		top: 0;
		margin-left: 40%;
		width: 60%;
		text-align: right;
	}
	.left-alt {
		width: 60%;
		align-items: left;
	}
	.right-alt {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 60%;
		display: flex;
		width: 40%;
		align-items: center;
		text-align: center;
	}
	.size-1 {
		font-size: 2rem;
	}
	.size-2 {
		font-size: 1.8rem;
	}
	.size-3 {
		font-size: 1.6rem;
	}
	.size-4 {
		font-size: 1.4rem;
	}
	.size-5 {
		font-size: 1.2rem;
	}

	@media only screen and (max-width: 600px) {
		.container {
			width: 80%;
		}
		.wrapped-3 {
			flex-direction: column;
		}
		.wrapped-4 {
			flex-direction: column;
		}
		.wrapped-5 {
			flex-direction: column;
		}
		.left {
			width: 100%;
			position: relative;
		}
		.right-alt {
			width: 100%;
			position: relative;
			left: 0;
		}
	}
</style>
