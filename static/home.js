function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    
    // Get form values
    var sqft = document.getElementById("uiSqft").value;
    var bhk = document.getElementById("uiBHK").value;
    var bathrooms = document.getElementById("uiBath").value;
    var location = document.getElementById("uiLocations").value;

    // Validate inputs
    if (!sqft || !bhk || !bathrooms || !location) {
        showError("Please fill in all required fields");
        return;
    }

    if (sqft < 100) {
        showError("Area must be at least 100 sqft");
        return;
    }

    if (bhk < 1 || bhk > 10) {
        showError("BHK must be between 1 and 10");
        return;
    }

    if (bathrooms < 1 || bathrooms > 10) {
        showError("Bathrooms must be between 1 and 10");
        return;
    }

    // Show loading state
    document.getElementById("uiEstimatedPrice").innerHTML = "<h3>🔄 Calculating price...</h3>";
    document.getElementById("uiEstimatedPrice").className = "loading";

    var url = "/predict_home_price";

    $.post(url, {
        sqft: parseFloat(sqft),
        bhk: parseInt(bhk),
        bath: parseInt(bathrooms),
        location: location
    }, function(data, status) {
        console.log("Price prediction successful:", data.estimated_price);
        showPrice(data.estimated_price);
    }).fail(function(xhr, status, error) {
        console.error("Error:", error);
        showError("Failed to get price prediction. Please try again.");
    });
}

function showPrice(price) {
    document.getElementById("uiEstimatedPrice").innerHTML =
        "<h2>🏠 Estimated Price: ₹ " + price.toString() + " Lakhs</h2>";
    document.getElementById("uiEstimatedPrice").className = "price-result";
}

function showError(message) {
    document.getElementById("uiEstimatedPrice").innerHTML = "<h3>❌ " + message + "</h3>";
    document.getElementById("uiEstimatedPrice").className = "error";
}

function onPageLoad() {
  console.log("document loaded");

  var url = "/get_location_names";
  $.get(url, function(data, status) {
      console.log("got response for get_location_names request");
      if(data) {
          var locations = data.locations;
          var uiLocations = document.getElementById("uiLocations");
          $('#uiLocations').empty();
          for(var i in locations) {
              var opt = new Option(locations[i]);
              $('#uiLocations').append(opt);
          }
      }
  });

  var url2 = "/api/get_area_names";
  $.get(url2, function(data, status) {
      console.log("got response for get_area_names request");
      if(data) {
          var area = data.area;
          var uiArea = document.getElementById("uiArea");
          $('#uiArea').empty();
          for(var i in area) {
              var opt = new Option(area[i]);
              $('#uiArea').append(opt);
          }
      }
  });

  var url3 = "/api/get_availability_names";
  $.get(url3, function(data, status) {
      console.log("got response for get_availability_names request");
      if(data) {
          var availability = data.availability;
          var uiAvailability = document.getElementById("uiAvailability");
          $('#uiAvailability').empty();
          for(var i in availability) {
              var opt = new Option(availability[i]);
              $('#uiAvailability').append(opt);
          }
      }
  });
}

window.onload = onPageLoad;
