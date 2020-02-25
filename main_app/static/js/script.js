//Open box with login and password
function openbox(id){
	let display = document.getElementById(id).style.display;
	if(display === 'none'){
	   document.getElementById(id).style.display='block';
	}
	else{
	  document.getElementById(id).style.display='none';
	}
}

//Open box with statistic
function open_statistic()
{
	let top = document.getElementById("block_with_statistic").style.top;
	if('0px' === top){
		document.getElementById("block_with_statistic").style.top='-100%';
		document.getElementById("statistic_button").style.marginTop='5px';
		document.getElementById("statistic_button").style.transform='rotate(45deg)';
		document.getElementById("body_statistic").style.marginTop='7px';
	}
	else {
		document.getElementById("block_with_statistic").style.top='0px';
		document.getElementById("statistic_button").style.transform='rotate(225deg)';
		document.getElementById("statistic_button").style.marginTop='20px';
		document.getElementById("body_statistic").style.marginTop='1px';
	}
}

//Change image
function change_image(){
	image.click()
	document.querySelector("#image").addEventListener("change", function () {
		if (this.files[0]) {
			fr = new FileReader();
			fr.addEventListener("load", function () {
				document.querySelector("#main_image").src = fr.result;
				}, false);
			fr.readAsDataURL(this.files[0]);
		}
	}
	);
}


function upload_article_image() {
	var inputs = document.querySelectorAll('.inputfile');
Array.prototype.forEach.call(inputs, function(input){
  var label	 = input.nextElementSibling,
      labelVal = label.innerHTML;
  input.addEventListener('change', function(e){
    var fileName = '';
    if( this.files && this.files.length > 1 )
      fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
    else
      fileName = e.target.value.split( '\\' ).pop();
		if( fileName )
      label.querySelector( 'span' ).innerHTML = fileName;
    else
      label.innerHTML = labelVal;
	});
});
}

window.onkeydown=function(event){
    if(event.keyCode===13){
        event.preventDefault();
    }
}
