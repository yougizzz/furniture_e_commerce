function show_product_detail_modal(id){
    const id_product = parseInt(id);
    $.ajax({
        url: '/product-modal/' + id_product,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            $('#modalPrice').text(data.price);
            $('#modalDetail').text(data.detail);
            $('#modalImage').attr('src', data.mainImage.url);
            $('#productModal').modal('show');
        },
        error: function () {
            alert('not found this product')
        }
    })
}