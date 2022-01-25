<script>
	function enumInput() {
        	let creds = {};
        	const inputs = ["username", "password"];
        	for (let i=0; i<inputs.length; i++){
			let value = document.querySelector(`[type=${inputs[i]}]`).value;
			if (!value){
				alert(`Please enter your: ${inputs[i]}`);
				return;
			}
                	creds[inputs[i]] = value;
        	}
        	return creds;
	}

	function login() {
		let creds = enumInput();
		if (creds) {
			fetch(`http://127.0.0.1:8888/select?username=${creds.username}`)
				.then(resp => resp.json()
				.then(data => {
					alert(`You're most welcome!\n\n${JSON.stringify(data)}`);
					document.location = "/"
				}
			));
		}
	}
</script>

<section class="section">
  <div class="card bg-indigo-400">
    <div class="card__header">
        <p class="font-bold px-3">Login</p>
    </div>
    <div class="content">
        <!-- Email -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Username:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="username" placeholder="us3rn4m3"></div>
		</div>
		<!-- Password -->
		<div class="row level">
		    <div class="col-xs-3 level-item">
		        <p class="m-0">Password:</p>
		    </div>
		    <div class="col-xs-9 level-item"><input type="password" placeholder="Pa*sw*rd h*re"></div>
		</div>
    </div>
    <div class="card__footer level content"><a href="#forgot-password">Forgot Password?</a></div>
    <div class="card__action-bar u-center">
        <button class="btn-dark outline" on:click={login}>Login</button>
    </div>

    <div class="modal modal-animated--zoom-in" id="forgot-password">
	<div class="model-content">
	    <div class="modal-body">
		    <h1>REMEMBER IT THEN!</h1>
	    </div>
        </div>
    </div>

  </div>
</section>

<style>
  .section {
    padding: 11em;
    margin: 0 auto;
  }
</style>
