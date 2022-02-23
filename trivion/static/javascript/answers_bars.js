var a = "small_square_red";
var b = "small_square_blue";
var c = "small_square_yellow";
var d = "small_square_green";
var arr1 = [a, b, c, d];
var arr2 = [document.getElementById("a").innerHTML, document.getElementById("b").innerHTML,
document.getElementById("c").innerHTML, document.getElementById("d").innerHTML];
for (i = 0; i < arr1.length; i++) {
    document.getElementsByClassName(arr1[i])[0].style.height = (70 + arr2[i] * 50) + "px";
}