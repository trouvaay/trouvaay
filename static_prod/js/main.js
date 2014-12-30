var TrendyRoom = {
    init : function() {
        this.resizeContent();
        this.placeLogo();
        this.initFlexslider();
        this.initIsotope();
        $('.quality-chooser a').on('click', this.qualitySelector);
        $('ul.colors .color').on('click', this.colorSelector);
        $('.form-checkbox-wrap a').on('click', this.customCheckbox);
        $('.radio-button').on('click', this.paymentTab);
        $('.product-slider').flexslider({
            animation: "slide",
            slideshow: false
        })
        $('.widget.leave-feedback a').on('click', function(event) {
            $('.widget.leave-feedback a.active').removeClass('active');
            $(this).addClass('active');

            var isLiked =  $(this).hasClass('like') ? true : false;
            $("#likes").val(isLiked);
            event.preventDefault();
        });
        $('select').selectBoxIt({
           autoWidth: false
        });
    },
    initIsotope : function() {
        var $container = $('.isotope-products').isotope({
            // options
            itemSelector : '.col-sm-6',
            layoutMode : 'fitRows'
        });
        $('.filters-wrapper a').click(function() {
            $('.filters-wrapper').find('.active').removeClass('active');
            var $el = $(this);
            $el.addClass('active');
            var selector = $el.attr('data-filter');
            $container.isotope({ filter: selector });
            return false;
        });
    },
    initFlexslider : function() {
        $('.homepage-slider').flexslider({
            animation: "slide",
            controlNav: true,
            directionNav : false,
            animationLoop: true,
            slideshow: false
        });
        $(".homepage-slider").delegate(".slides > li", "click", function () {
            var activeIndex = $(".homepage-slider li.flex-active-slide").index();
            var clickIndex = $(this).index();
            if(activeIndex > clickIndex) {
                $(".homepage-slider").flexslider("prev");
            }
            if(activeIndex < clickIndex) {
                $(".homepage-slider").flexslider("next");
            }
        });
    },
    placeLogo : function() {
        if($(window).width() > 767) {
            $('.navbar .navbar-brand').outerHeight($('.navbar .right-side').height());
        } else {
            $('.navbar .navbar-brand').outerHeight($('.navbar .navbar-brand img').height());
        }
    },
    resizeContent : function() {
    },
    qualitySelector : function(event) {
        var el = $(this);
        var inc = 1;
        if(el.hasClass('less')) {
            inc = -1;
        }
        var qualityValue = parseInt($('.quality-chooser input').val());
        qualityValue = qualityValue + inc;
        if(qualityValue < 1) {
            qualityValue = 1;
        }
        $('.quality-chooser input').val(qualityValue);
        event.preventDefault();
    },
    colorSelector : function(event) {
        var colors = $('ul.colors .color').closest('.color-chooser').find('.color');

        colors.removeClass('active');
        $(this).addClass('active');

        var value = $(this).attr('data-value');
        $(this).prev().val(value);

        var imageUrl = $(this).attr('data-image');
        var image = $(this).closest('.product').find('img');
        image.attr('src', imageUrl);

        event.preventDefault();
    },
    customCheckbox : function(event) {
        var input = $('#same-info');
        var currentVal = input.val();
        var icon = $('.form-checkbox-wrap a .fa-check');
        if(currentVal == 'true') {
            input.val('false');
            icon.css("display", "none");
        } else {
            input.val('true');
            icon.css("display", "block");
        }
        event.preventDefault();
    },
    paymentTab : function() {
        var inputValue = $(this).attr('data-value');
        $('#payment-type').val(inputValue);

        $('.radio-button').removeClass('checked');
        $(this).addClass('checked');
    }
};
$(document).ready(function() {
    TrendyRoom.init();
});
$(window).resize(function() {
    TrendyRoom.resizeContent();
    TrendyRoom.placeLogo();
});