$().ready(function(){
//    alert("Hello!");

    $('imgID').click(function(){
        alert("yess!");
        alert($(this).attr('alt'));
   });

    // On 1st page load set content on index page and update activeID value to 0
    if ($('#activeID').val() == 1)
    {
        loadContent("Includes/_latitude.html", true);
        $('#activeID').val(0);
    }

    // Navigation: set active link on-click & load content 
    $('.nav-link').on('click',function() {
        alert("navigating!");

        //Set active link on click
        $('#navID').find("*").removeClass('active');
        $(this).addClass("active");
        alert("1st: " + $(this).text());     
        eval_link($(this).text());
    });

    // Load content for dropdown links in Nav tab
    $("#plotID a").click(function() {
        alert("plot!");
        eval_link($(this).text());
      });

    // $("#imgID div a").click(function() {
    //     alert("image!")
    //     $('#navID').find("*").removeClass('active');
    //     $("#navbardrop").addClass("active");
    //     alert($(this).attr('title'))
    //     eval_link($(this).attr('title'));
    //     //Set active link on click

    //     // alert($("#navbardrop").attr('class')); $(this).find("a").attr("href"); 
    // });
      
    //Evaluate the link type and load the correct file
    function eval_link(_value) {
        // alert("work");
        //load content based on clicked button
        switch(_value) {
            case "Latitude":
                alert("Eval: " + _value);   
                loadContent("Includes/_latitude.html", false);
                break;
            case "Comparison":
                loadContent("Includes/_comparison.html", false);
                break;         
            case "Data":
                loadContent("Includes/_data.html", false);
                break;
            case "Max Temperature":
            case "temperature image":
                loadContent("Includes/_maxtemp.html", true);
                break;
            case "Humidity":
            case "Humidity Visualization":
                loadContent("Includes/_humidity.html", true);
                break;            
            case "Cloudiness":
            case "Cloudiness Visualization":
                loadContent("Includes/_cloudiness.html", true);
                break;
            case "Wind Speed":
            case "Wind Speed Visualization":
                loadContent("Includes/_windspeed.html", true);
                break;
       }     
     }    

    //If content exist, remove & load new else just load new
    function loadContent(_link, _loadweather) {
        if ( $("#contentID").children().length > 0 ) {
            $("#contentID").empty();
        } 
        //Load content  
        $("#contentID").load(_link, function(responseTxt, statusTxt, xhr){
            // If loading is successful and load weather is true load weather images also, else alert with error
            alert("Load");   
            if(statusTxt == "success")
                if (_loadweather == true)  
                    loadWeather("Includes/_weather.html"); 
            if(statusTxt == "error")
                alert("Error: " + xhr.status + ": " + xhr.statusText);
          });    
     }    
 
    //Load all weather images
    function loadWeather(_link) {
        // alert("Load Weather.");
        $("#weatherID").load(_link);          
     }
    
  
});