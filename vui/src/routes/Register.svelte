<script>

	function enumInput() {
        	let creds = {};
        	const inputs = ["name", "username", "email", "tel", "address", "password"];
        	for (let i=0; i<inputs.length; i++){
                	creds[inputs[i]] = document.querySelector(`[type=${inputs[i]}]`).value;
        	}
        	return creds;
	}

	function register() {
		// TODO: import this function instead.
		let creds =  enumInput();
		// TODO: Remove these hardcoded URLs.
		fetch('http://127.0.0.1:8888/user', {
			method: "PUT",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(creds)
		})
		.then(resp => resp.json())
		.then(data => {
			if ( data['resp'] === 'done' ) {
				alert("User sucessfully registered!");
				document.location = "/login";
			}
			})
		.catch(error => console.error(error))
	}
</script>

<section class="section">
  <div class="card bg-indigo-400">
    <div class="card__header">
        <p class="font-bold px-3">Register</p>
    </div>
    <div class="content">
                <!-- Name -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Name:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="name" placeholder="John Doe"></div>
		</div>
		<!-- Username -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Username:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="username" placeholder="us3rn4m3"></div>
		</div>
		<!-- Email -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Email:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="email" placeholder="hi@john.me"></div>
		</div>
		<!-- Tel -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Phone number:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="tel" placeholder="+977 97x8x69x3x"></div>
		</div>
		<!-- Address -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
			<p class="m-0">Address:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="address" placeholder="Your Physical address."></div>
		</div>
		<!-- Password -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Password:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="password" placeholder="Pa*sw*rd h*re"></div>
		</div>
    </div>
    <div class="card__action-bar u-center">
        <button class="btn-dark outline" on:click={register}>Register</button>
    </div>
  </div>
</section>


<style>
  .section {
    padding: 11em;
    margin: 0 auto;
  }
</style>
