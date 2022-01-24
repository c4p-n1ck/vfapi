<script>
	let lusername;
	let lpassword;
	let username;
	let password;
	let name;
	let email;
	let tel;
	let address;

	function register() {
		if ( name && username && email && address && tel && password ) {
		    let creds = {
			    name: name,
			    username: username,
			    email: email,
			    address: address,
			    tel: tel,
			    password: password
		    };
		    // TODO: Remove hardcoded URLs.
		    fetch("http://127.0.0.1:8888/user", {
			    method: "PUT",
			    headers: {"Content-Type": "application/json"},
			    body: JSON.stringify(creds)
		    })
		    .then(resp => resp.json())
		    .then(data => {
			    if ( data['resp'] === 'done' ) {
				    alert(`User ${creds.username} has been sucessfully registered!`);
				    document.location = "/login";
			    }
		    })
		    .catch(err => console.error(err));
		}
	}

	function login() {
		if ( lusername && lpassword ) {
			let creds = {"username": lusername, "password": lpassword};
			fetch(`http://127.0.0.1:8888/select?username=${creds.username}`)
			.then(resp => resp.json())
			.then(data => {
				alert(`You're most welcome!\n\n${JSON.stringify(data)}`);
				document.location = "/";
			})
			.catch(err => console.error(err));
		}
	}
</script>

<div class="hero fullscreen">
    <div class="hero-body">
        <div class="content">
            <div class="frame padded">
                <div class="space large"></div>
                <div class="frame__body p-0">
                    <div class="row p-0 level fill-height">
                        <div class="col-6">
			    <!-- <form name="login-form" method="post"> -->
                                <div class="frame__body">
                                    <h3>Login</h3>
                                    <div class="form-section">
                                        <label>Username</label>
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="username" name="username" placeholder="us3rn4m3" type="text" bind:value={lusername}/>
                                            <span class="icon">
                                                <i class="far fa-wrapper fa-user small"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <label>Password</label>
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="password" name="password" placeholder="Password" type="password" bind:value={lpassword}/>
                                            <span class="icon">
                                                <i class="fas fa-wrapper fa-key small"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div class="space"></div>
                                    <button class="btn-info u-pull-right" name="btn" value="login" type="submit" on:click={login}>Log In</button>
                                    <span class="fg-danger info"></span>
                                    <a href="#forgot-password-model" class="u u-LR">Forgot password?</a>
                                </div>
			    <!-- </form> -->
                        </div>
                        <div class="col-6">
			    <!-- <form name="register-form" method="post"> -->
                                <div class="padded">
                                    <h3>Sign Up</h3>
                                    <div class="form-section">
                                        <label>Your details</label>
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="name" name="name" placeholder="Name" type="text" bind:value={name}>
                                            <span class="icon">
                                                <i class="far fa-wrapper fa-user-circle small"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="username" name="username" placeholder="us3rn4m3" type="text" bind:value={username}>
                                            <span class="icon">
                                                <i class="far fa-wrapper fa-user small"></i>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="register-email" name="email" placeholder="Email" type="text" bind:value={email}>
                                            <span class="icon">
                                                <i class="far fa-wrapper fa-envelope-open small"></i>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="address" name="address" placeholder="Address" type="text" bind:value={address}>
                                                <span class="icon">
						    <i class="fas fa-wrapper fa-map-marker-alt small"></i>
						</span>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="tel" name="tel" placeholder="+9x7 9x2x69x8x3" type="text" bind:value={tel}>
                                                <span class="icon">
						    <i class="fas fa-wrapper fa-mobile small"></i>
						</span>
                                        </div>
                                    </div>
                                    <div class="form-section">
                                        <div class="input-control">
                                            <input class="input-contains-icon" id="register-password" name="password" placeholder="Password" type="password" bind:value={password}>
                                            <span class="icon">
                                                <i class="fas fa-wrapper fa-key small"></i>
                                        </div>
                                    </div>
                                    <button class="btn-info u-pull-right" name="btn" value="register" type="submit" on:click={register}>Sign Up</button>
                                    <span class="fg-danger info"></span>
                                </div>
			    <!-- </form> -->
                        </div>
                    </div>
                </div>
                <div class="space large"></div>
		</div>
        </div>
    </div>
</div>


<style>
        body {
                background: #C9D6FF;  /* fallback for old browsers */
                background: -webkit-linear-gradient(to bottom, #E2E2E2, #C9D6FF);  /* Chrome 10-25, Safari 5.1-6 */
                background: linear-gradient(to bottom, #E2E2E2, #C9D6FF) no-repeat fixed; /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
            }

            .frame {
                background-color: #fff;
            }

            .padded {
                padding: 0 2rem;
            }

            .level.fill-height {
                -webkit-box-align: stretch;
                -ms-flex-align: stretch;
                align-items: stretch;
                display: -ms-flexbox;
                display: flex;
            }

            .col:first-child {
                padding-left: 0;
            }

            .col:last-child {
                padding-right: 0;
            }

            ul {
                display: flex;
                list-style: none;
            }

            li {
                align-items: center;
                display: flex;
                padding: 0 0.5rem;
            }

            @media screen and (min-width: 769px) {    
                .col-6:not(:last-child) {
                    border-right: 1px solid rgba(0, 0, 0, 0.10);
                }
            }

            @media screen and (max-width: 768px) {
                .level.fill-height {
                    display: inherit;
                }
            }
</style>
