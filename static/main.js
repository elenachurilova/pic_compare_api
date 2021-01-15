"use strict";

function getPercentage(evt) {

    evt.preventDefault();

    console.log("Collecting user input")

    const userInput = {
        'image_one' : $("#image_one_input").val(),
        'image_two' : $("#image_two_input").val()
    }

    const userInputJson = JSON.stringify(userInput)

    console.log("Sending user input to the server")

    $.ajax({
        type: "POST",
        url: '/api/compare.json',
        data: userInputJson,
        success: (res) => {

            $("#result_message").append(`<h3>These images are ${res['result']}% similar</h3>`)
            $("#image_one").append(`<img src="${userInput['image_one']}" alt="First image">`)
            $("#image_two").append(`<img src="${userInput['image_two']}" alt="Second image">`)
        },
        dataType: "json",
        headers: {"Content-Type" : "application/json"},
    });

    // $.post(`/api/compare.json`, userInput, (res) => {
    //         console.log("Received a response from server")
    //         console.log(res)
    //         $("#result_message").append(`<h3>These images are ${res['result']}% similar</h3>`)
    //     } 
    // )
    
    // $("#image_one").append(`<img src="${userInput['image_one']}" alt="First image">`)
    // $("#image_two").append(`<img src="${userInput['image_two']}" alt="Second image">`)
}

//event: clicking on Submit button...
$("#get-percentage").on("click", getPercentage);