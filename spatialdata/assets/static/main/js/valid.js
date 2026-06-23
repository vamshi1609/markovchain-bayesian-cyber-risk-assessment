function validateLForm(){

    var email = document.myform.email
    var emailpattern = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([com\co\.\in])+$/; // to validate email id
    var password = document.myform.pwd
  
  
    if (email.value.length <= 0) {
      Swal.fire("Email ID missing","Enter your email ID", "warning");
      email.focus();
      return false;
      
      }
      if(!email.value.match(emailpattern)){
      Swal.fire("Retype your email", "Invalid Email format", "warning"); 
      email.focus();            
      return false;
      }
      if (password.value.length <= 0) {
      Swal.fire("Password missing", "Enter your password", "warning");
      password.focus();
      return false;
      
      }
      return true;
    }



    function validateRForm(){
        var username = document.myform.name
        var email = document.myform.email
        var emailpattern = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([com\co\.\in])+$/; // to validate email id
        var contact = document.myform.phone
        var password = document.myform.pwd
    
        var letter = /[a-z]/;
        var upper = /[A-Z]/;
        var number = /[0-9]/;   
        var image = document.myform.image
        
      
      
      
        if (username.value.length <= 0) {
        Swal.fire(" Name can't be blank", "", "warning");
        username.focus();
        return false;
        
        }
        
        if (contact.value.length <= 0) {
        Swal.fire("Enter your mobile number","", "warning");
        contact.focus();
        return false;
        
        }
        if(isNaN(contact.value)){
        Swal.fire("Invalid Mobile number","", "warning");
        return false;
        }
        if(contact.value.length=="" || contact.value.length!=10){
        Swal.fire("Invalid Mobile number","", "warning");
        return false;
        }
      
        if (email.value.length <= 0) {
        Swal.fire("Enter your email ID","", "warning");
        email.focus();
        return false;
        
        }
        if(!email.value.match(emailpattern)){
        Swal.fire("Invalid Email format","", "warning"); 
        email.focus();            
        return false;
        }
        if (password.value.length <= 0) {
        Swal.fire("Enter your password","", "warning");
        password.focus();
        return false;
        
        }
        if (!letter.test(password.value)) {
        Swal.fire("Please make sure password includes a lowercase letter.","", "warning");
        password.focus();
        return false;
        
        }
        if (!upper.test(password.value)) {
        Swal.fire("Please make sure password includes a uppercase letter.","", "warning");
        password.focus();
        return false;
        
        }
        if (!number.test(password.value)) {
        Swal.fire("Please make sure password Includes a digit.","", "warning");
        password.focus();
        return false;              
        }
       
      
       
      
        if (image.value.length == "") {
        Swal.fire("Upload profile Picture","", "warning");
        image.focus();
        return false;
        
        }
      }
    
    
    