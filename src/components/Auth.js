export function enumInput(isLogin=false) {
	var creds = {};
	if (isLogin) {
		var inputs = ["username", "password"];
	} else {
		var inputs = ["name", "username", "password", "email", "tel", "address"];
	} for (let i=0; i < inputs.length; i++ ) {
		value = document.querySelector(`[name=${inputs[i]}]`).value;
		if (!value) {
			alert(`Please do enter your ${inputs[i]}`);
			return;
		} creds[inputs[i]] = value;
	} return creds;
}
