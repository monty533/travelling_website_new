$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$(".plus-cart ").click(function(){
    var prod_id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            prod_id:prod_id
        },
        success:function(response){
            console.log('monty succes',response);
            eml.innerText = response.quantity;
            document.getElementById("amount").innerText = response.amount;
            document.getElementById("total_amount").innerText = response.total_amount;
        },
        error:function(){
            console.log('monty error');
        }
    })
});

$(".minus-cart ").click(function(){
    var prod_id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{
            prod_id:prod_id
        },
        success:function(response){
            eml.innerText = response.quantity;
            document.getElementById("amount").innerText = response.amount;
            document.getElementById("total_amount").innerText = response.total_amount;
        },
        error:function(){
        }
    })
});

$(".remove-cart ").click(function(){
    var prod_id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type:'GET',
        url:'/removecart',
        data:{
            prod_id:prod_id
        },
        success:function(response){
            document.getElementById("amount").innerText = response.amount;
            document.getElementById("total_amount").innerText = response.total_amount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
        },
        error:function(){
        }
    })
});