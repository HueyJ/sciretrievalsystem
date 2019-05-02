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
		if (loadHeight > documentHeight	&& currPage() < $('#page').text()) {
            if (scroll) {
                $.get(
					"/aquery/" + $("title").html() + "/" + nextPage(),
					function(response) {
						results = JSON.parse(response)

						for (var i = 0; i < results.length; i++) {
							$("#result-list").append(

							)
						}

						// prevent duplicate operation
						scroll = false;
					}
				)
				// restore to enable pagination
				// scroll = true;
            }
		}
	});

	$("#search").on('input propertychange', function(event){
		query_expression = "/" + encodeURIComponent($("#search").val());
		query_expression = query_expression.replace(".", "&#46");
		$("form").attr("action", "/query" + query_expression);
	});

	function currPage() {
		return curr_page;
	}

	function nextPage() {
		return ++curr_page
	}

	function renderResult(result) {
		if (parseInt(result.openaccess)) {
			panelTheme = "panel-success"
			
		} else {
			panelTheme = "panel-default"
		}
		r = "" +
		"<div class='panel " + panelTheme + "'>"  +
			// Default panel contents
			"<div class='panel-heading'>Panel heading</div>" +
			"<div class='panel-body'>" +
				"<p>...</p>" +
			"</div>" +
			// List group
			"<ul class='list-group'>" +
				"<li class='list-group-item'>Cras justo odio</li>" +
				"<li class='list-group-item'>Dapibus ac facilisis in</li>" +
				"<li class='list-group-item'>Morbi leo risus</li>" +
				"<li class='list-group-item'>Porta ac consectetur ac</li>" +
				"<li class='list-group-item'>Vestibulum at eros</li>" +
			"</ul>" +
			"<div class='panel-footer'>Panel footer</div>" +
		"</div>"
	}

});
