var xmlhttp, timer_req, url, param;
    
function aplicaCW()

{

 var index;

  xmlhttp=GetXmlHttpObject();
  if (xmlhttp==null)
   {
    alert ("Browser does not support HTTP Request");
    return;
   }

var locationNameId = document.getElementById('locationName');
var locationName = (locationNameId.innerText || locationNameId.textContent);

var cw1="", cw2="", mode="";


 if (document.getElementById('freeCooling').checked)
    mode = "freeCooling";
 if (document.getElementById('autoMode').checked)
   {
   mode = "auto";
   ONOFF1 = document.getElementById("rel1_1").selectedIndex;
   ONOFF2 = document.getElementById("rel2_1").selectedIndex;
   
   range1 = document.getElementById("rel1_2").selectedIndex;
   range2 = document.getElementById("rel2_2").selectedIndex;

   sensor1 = document.getElementById("rel1_3").selectedIndex;
   sensor2 = document.getElementById("rel2_3").selectedIndex;

   if ( (ONOFF1 == 0) || (ONOFF1 == 0) || (range1 ==0) || (range2 == 0) || (sensor1 == 0) || (sensor2 == 0) )
    {
     alert("Selectati toti parametrii pentru ambele contacte.");
     return;
     };

   cw1 = ONOFF1 + ':' + range1 + ':' + sensor1;  
   cw2 = ONOFF2 + ':' + range2 + ':' + sensor2;

   };

 url="aplicacw.php?locationName=" +locationName + "&mode=" + mode + "&cw1="+ cw1 + "&cw2="+cw2;

 url=url+"&ran="+Math.random();

 xmlhttp.onreadystatechange=afisareRezultateAplica;
 xmlhttp.open("GET",url,true);
 xmlhttp.send(null);


};


function manual(port, status){

var index;

  xmlhttp=GetXmlHttpObject();
  if (xmlhttp==null)
   {
    alert ("Browser does not support HTTP Request");
    return;
   }




 var locationNameId = document.getElementById('locationName');
 var locationName = (locationNameId.innerText || locationNameId.textContent);

 var mode = "manual";

 url="aplicacw.php?locationName=" +locationName + "&mode=" + mode+ "&port="+port +"&status=" + status ; // atat !
 url=url+"&ran="+Math.random();

 xmlhttp.onreadystatechange=afisareRezultateAplica;
 xmlhttp.open("GET",url,true);
 xmlhttp.send(null);





 }



function afisareRezultateAplica()
{
	
 if (xmlhttp.readyState==4)
 {
//  alert(xmlhttp.responseText); 
 }
}


function GetXmlHttpObject()
{
if (window.XMLHttpRequest)
{
// code for IE7+, Firefox, Chrome, Opera, Safari
return new XMLHttpRequest();
}
if (window.ActiveXObject)
{
// code for IE6, IE5
 return new ActiveXObject("Microsoft.XMLHTTP");
}
return null;
}


