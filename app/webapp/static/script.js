$(document).ready(function() {
	// Show or hide the sticky footer button
	$(window).scroll(function() {
		if ($(this).scrollTop() > 200) {
			$('.go-top').fadeIn(200);
		} else {
			$('.go-top').fadeOut(200);
		}
	});

	// Animate the scroll to top
	$('.go-top').click(function(event) {
		event.preventDefault();

		$('html, body').animate({scrollTop: 0}, 300);
	})

	$("#b01").click(function(){
		htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});
		$("#myDiv").html(htmlobj.responseText);
	});
});


class Pagination {

	constractor(totalNum, perPage, currPage) {
		this.totalNum = totalNum
		this.perPage = perPage
		this.currPage = currPage
		this.pageNum = parseInt(Math.ceil(this.totalNum / parseFloat(this.perPage)))
	}

	function getPageNum() {
		return this.pageNum
	}

	function nextPage() {
		if this.hasNext() {

		}
	}

    function hasPrev() {
		return this.currPage > 1
	}

	function hasNext() {
		return this.page < this.pageNum
	}

	function

}
