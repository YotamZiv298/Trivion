var timer = setInterval(function(){
    timeleft--;
    document.getElementById("countdowntimer").textContent = timeleft;
    if(timeleft == 0)
    {
        clearInterval(timer);
        window.location.replace("/game/" + window.location.pathname.split('/')[2] + "/" + PIN.toString() + "/question" + question_number + "/results" + "?timer=" + time_original);
    }
},1000);