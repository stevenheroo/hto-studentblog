const showPasswordToggle = document.querySelector(".showPasswordToggle");
const changePasswordToggle = document.querySelector(".changePasswordToggle");
const resetPasswordToggle = document.querySelector(".resetPasswordToggle");
const inputPassword = document.querySelector("#inputPassword");
const inputPassword2 = document.querySelector("#inputPassword2");

const id_old_password = document.querySelector("#id_old_password");
const id_new_password1 = document.querySelector("#id_new_password1");
const id_new_password2 = document.querySelector("#id_new_password2");


//Toggle for Login/Signup Screen...
const handleToggleInput=(e)=>{
	if (showPasswordToggle.textContent==='ShowPassword') {
		showPasswordToggle.textContent = "HidePassword";

		//If show, update Inputpassword field to text

		//Login screen
		inputPassword.setAttribute("type", "text");
		inputPassword2.setAttribute("type", "text");

	}
	else{
		showPasswordToggle.textContent = "ShowPassword";

		//If hide, update password field not visible
		inputPassword.setAttribute("type", "password");
		inputPassword2.setAttribute("type", "password");
	}
}



//Toggle for Change Password Screen...
const handleToggle_changePassword=(e)=>{
	if (changePasswordToggle.textContent==='ShowPassword') {
		changePasswordToggle.textContent = "HidePassword";

		//If show_password ,then change to text
		id_old_password.setAttribute("type", "text");
		id_new_password1.setAttribute("type", "text");
		id_new_password2.setAttribute("type", "text");

	}
	else{
		changePasswordToggle.textContent = "ShowPassword";

		//If hide_password ,then change text hidden
		id_old_password.setAttribute("type", "password");
		id_new_password1.setAttribute("type", "password");
		id_new_password2.setAttribute("type", "password");

	}
}



//Toggle for Password Reset Confirm Screen...
const handleToggle_resetPassword=(e)=>{
	if (resetPasswordToggle.textContent==='ShowPassword') {
		resetPasswordToggle.textContent = "HidePassword";

		//If show_password ,then change to text
		id_new_password1.setAttribute("type", "text");
		id_new_password2.setAttribute("type", "text");

	}
	else{
		resetPasswordToggle.textContent = "ShowPassword";

		//If hide_password ,then change text hidden
		id_new_password1.setAttribute("type", "password");
		id_new_password2.setAttribute("type", "password");

	}
}



showPasswordToggle.addEventListener('click',handleToggleInput);
changePasswordToggle.addEventListener('click',handleToggle_changePassword);
resetPasswordToggle.addEventListener('click',handleToggle_resetPassword);