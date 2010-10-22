function validate() {
  var inputName = document.getElementById("name");
  var inputEmail = document.getElementById("email");
  var inputComment = document.getElementById("comment");
  
  validateName = validateInput(inputName);
  validateEmail = validateInputEmail(inputEmail);        
  validateComment = validateInput(inputComment);       

  if (validateName && validateEmail && validateComment)
    return true;
  else
    return false;
}

function validateInput(control) {
  var result = true;
  if (control.value == null || control.value == "") {
    control.style.border = "solid 1px #c8191e";
    result = false;
  }
  else {
    control.style.border = "solid 1px #999";
  }
  return result;
}

function validateInputEmail(control) {
  var result = true;
  if (control.value == null || control.value == "") {
    control.style.border = "solid 1px #c8191e";
    result = false;
  }
  else {
    if ((control.value.indexOf(".") > 2) && (control.value.indexOf("@") > 0)) {
      control.style.border = "solid 1px #999";
    }
    else {
      control.style.border = "solid 1px #c8191e";
      result = false;
    }
  }

  return result;
}