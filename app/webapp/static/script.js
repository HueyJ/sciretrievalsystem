$(document).ready(function() {

	var currPage = 0;
	var scrolled = false;
	var scroll = true;

	if (!$("#result").html() && $("#result-list").html()) {
		getCurrResults();
	}

	$(window).scroll(function() {
		// location of top
		var scrollTop = $(window).scrollTop();
		// height of window
		var windowHeight = $(window).height();
		// height of document
		var documentHeight = $(document).height();
		// 100 before touch the bottom
		var loadHeight = scrollTop + windowHeight + 100;
		toggleGoTop(scrollTop, loadHeight, documentHeight)
		if (loadHeight >= documentHeight && currPage < $("#page").text()) {
            if (scroll) {
				if (!scrolled) {
					scrolled = true;
				}
				getCurrResults();
            }
		}
		if (loadHeight >= documentHeight && currPage == $('#page').text()
			&& scroll) {
			$("#result-list").append(
				"<div " +
					"class='alert alert-warning alert-dismissible fade in' " +
					"role='alert'>" +
					"<button " +
						"type='button'" +
						"class='close'" +
						"data-dismiss='alert'" +
						"aria-label='Close'>" +
						"<span aria-hidden='true'>×</span>" +
					"</button>" +
					"<strong>It is the end!</strong>" +
				"</div>"
			);
			// end of all the results, never scroll down again.
			if (scroll) {
				scroll = false;
			}
		}
	});

	// display or hide go-top buttons
	function toggleGoTop(scrollTop, loadHeight, documentHeight) {
		if (scrollTop > 200) {
			$('.go-top').fadeIn(300);
		} else if (loadHeight >= documentHeight || scrollTop <= 200) {
			$('.go-top').fadeOut(300);
		}
	}

	function getCurrResults() {
		// lock scroll
		if (scroll) {
			scroll = false;
		}
		$.get(
			"/aquery/" + $("title").html() + "/" + nextPage(),
			function(response) {
				var results = JSON.parse(response);
				var rendering = "";

				for (var i = 0; i < results.length; i++) {
					rendering += renderResult(results[i]._source);
				}
				$("#result-list").append(
					"<div id='page" + currPage + "' hidden>" +
						rendering +
					"</div>"
				);
				$("#page" + currPage).fadeIn(300);
				// release lock
				if (!scroll) {
					scroll = true;
				}
			}
		);

	}

	function nextPage() {
		return ++currPage;
	}

	function renderResult(result) {
		if (parseInt(result.openaccess)) {
			theme = "-success";
			openaccess = "Open access"
		} else {
			theme = "-default";
			openaccess = "Abstract only"
		}

		id = result.id;
		href = result.href;
		title = result.title;
		author = result.author;
		abstract = result.abstract;
		subject = result.subject;

		r = "" +
		"<div id='result' class='panel panel" + theme + "'>"  +
			// Default panel contents
			"<div class='panel-heading'>" +
				"<h3 class='panel-title'>" +
					"<a href='" + href + "'>" +
						title +
					"</a>" +
				"</h3>" +
			"</div>" +
			// List group
			"<ul class='list-group'>" +
				"<li class='list-group-item'>" + author + "</li>" +
			"</ul>" +
			"<div class='panel-body'>" +
				"<a " +
					"data-toggle='collapse'" +
					"href='#" + id + "-abstract'>" +
					"Abstract" +
				"</a>" +
				"<br>" +
				"<div id='" + id + "-abstract' class='collapse'>" +
					abstract +
				"</div>" +
			"</div>" +

			"<div class='panel-footer'>" + subject + "</div>" +
		"</div>";
		return r;
	}

	// Animate the scroll to top
	$('.go-top').click(function(event) {
		event.preventDefault();

		$('html, body').animate({scrollTop: 0}, 300);
	});

	$("#search").on('input propertychange', function(event){
		query_expression = "/" + encodeURIComponent($("#search").val());
		query_expression = query_expression.replace(".", "&#46");
		$("form").attr("action", "/query" + query_expression);
	});

});
