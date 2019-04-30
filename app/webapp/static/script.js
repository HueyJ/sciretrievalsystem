$(document).ready(function() {
	// Show or hide the sticky footer button
	$(window).scroll(function() {
		if ($(this).scrollTop() > 200) {
			$('.go-top').fadeIn(300);
		} else {
			$('.go-top').fadeOut(300);
		}
	});

	// Animate the scroll to top
	$('.go-top').click(function(event) {
		event.preventDefault();

		$('html, body').animate({scrollTop: 0}, 300);
	})

	var curr_page = 1
	var scrolled = false
	var scroll = true

	$(window).scroll(function() {
		var scrollTop = $(window).scrollTop();
		var windowHeight = $(window).height();
		var documentHeight = $(document).height();
		var loadHeight = scrollTop + windowHeight + 125
		if (loadHeight > documentHeight && $('#page').text() != getPageNum()
				&& getPageNum() < $('#page').text()) {
            if (scroll) {
                $.get(
					"/aquery/" + $("title").html() + "/" + getPageNum(),
					function(results) {
						console.log(results)
						scroll = false;
					}
				)
				scroll = true;
            }
		}
	});

	function getPageNum() {
		if (scrolled) {
			return ++curr_page
		} else {
			scrolled = true;
			return curr_page;
		}
	}

});

$("#search").on('input propertychange', function(event){
	query_expression = "/" + $("#search").val();
	$("form").attr("action", "/query" + query_expression);
});


//
// class Pagination {
//
// 	constractor(totalNum, perPage, currPage) {
// 		this.totalNum = totalNum
// 		this.perPage = perPage
// 		this.currPage = currPage
// 		this.pageNum = parseInt(Math.ceil(this.totalNum / parseFloat(this.perPage)))
// 	}
//
// 	function getPageNum() {
// 		return this.pageNum
// 	}
//
// 	function nextPage() {
// 		if this.hasNext() {
//
// 		}
// 	}
//
//     function hasPrev() {
// 		return this.currPage > 1
// 	}
//
// 	function hasNext() {
// 		return this.page < this.pageNum
// 	}
//
// 	function
//
// }
